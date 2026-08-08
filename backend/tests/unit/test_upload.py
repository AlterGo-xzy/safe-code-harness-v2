from __future__ import annotations

import io
import stat
import zipfile
from pathlib import Path
from types import SimpleNamespace

import pytest

import safe_code_harness.workspaces.registry as registry_module
from safe_code_harness.workspaces.registry import WorkspaceRegistry
from safe_code_harness.workspaces.upload import ArchiveRejectedError, UploadLimits, _member_path


def zip_bytes(*members: tuple[str, bytes], symlink: bool = False) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in members:
            if symlink:
                entry = zipfile.ZipInfo(name)
                entry.create_system = 3
                entry.external_attr = (stat.S_IFLNK | 0o777) << 16
                archive.writestr(entry, content)
            else:
                archive.writestr(name, content)
    return buffer.getvalue()


def test_creates_a_unique_workspace_and_extracts_safe_files(tmp_path: Path) -> None:
    registry = WorkspaceRegistry(tmp_path)

    first = registry.create_from_zip(zip_bytes(("src/main.py", b"print('ok')")))
    second = registry.create_from_zip(zip_bytes(("README.md", b"safe project")))

    assert first.id != second.id
    assert first.root.parent == tmp_path.resolve()
    assert (first.root / "src" / "main.py").read_bytes() == b"print('ok')"
    assert registry.get(first.id) == first


@pytest.mark.parametrize(
    ("member_name", "expected_code"),
    [
        ("../outside.txt", "unsafe_archive_path"),
        ("/absolute.txt", "unsafe_archive_path"),
        ("C:/windows.txt", "unsafe_archive_path"),
        ("safe.txt:payload", "unsafe_archive_path"),
        (".env", "protected_archive_path"),
        (".git/config", "protected_archive_path"),
        ("config/api_key.txt", "protected_archive_path"),
        ("node_modules/package.json", "protected_archive_path"),
        (".pytest_cache/v/cache/nodeids", "protected_archive_path"),
    ],
)
def test_rejects_unsafe_member_names_without_creating_a_workspace(
    tmp_path: Path, member_name: str, expected_code: str
) -> None:
    registry = WorkspaceRegistry(tmp_path)

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(zip_bytes((member_name, b"content")))

    assert raised.value.code == expected_code
    assert list(tmp_path.iterdir()) == []


def test_rejects_symlink_members_before_extraction(tmp_path: Path) -> None:
    registry = WorkspaceRegistry(tmp_path)

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(zip_bytes(("linked", b"../outside"), symlink=True))

    assert raised.value.code == "unsafe_archive_member"
    assert list(tmp_path.iterdir()) == []


def test_rejects_members_that_normalize_to_the_same_target(tmp_path: Path) -> None:
    registry = WorkspaceRegistry(tmp_path)
    archive = zip_bytes(("src//main.py", b"first"), ("src/main.py", b"second"))

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(archive)

    assert raised.value.code == "duplicate_archive_member"
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    "member_name",
    [
        r"\\server\share\file.txt",
        r"..\escape.txt",
        r"safe\child.txt:payload",
        "NUL",
        "com1.txt",
        "folder/name.",
        "folder/name ",
    ],
)
def test_rejects_platform_ambiguous_member_paths(member_name: str) -> None:
    with pytest.raises(ArchiveRejectedError, match="unsafe_archive_path"):
        _member_path(member_name)


def test_rejects_nul_member_path_before_path_conversion() -> None:
    with pytest.raises(ArchiveRejectedError, match="unsafe_archive_path"):
        _member_path("safe\x00name.txt")


def test_rejects_archives_with_too_many_directory_or_file_members(tmp_path: Path) -> None:
    registry = WorkspaceRegistry(tmp_path, limits=UploadLimits(max_files=2))
    archive = zip_bytes(("one/", b""), ("two/", b""), ("safe.txt", b"content"))

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(archive)

    assert raised.value.code == "too_many_files"
    assert list(tmp_path.iterdir()) == []


def test_translates_unexpected_extraction_error_and_cleans_new_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = WorkspaceRegistry(tmp_path)

    def fail_extract(*_args: object, **_kwargs: object) -> int:
        raise FileExistsError("host path must not escape")

    monkeypatch.setattr(registry_module, "extract_verified_zip", fail_extract)

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(zip_bytes(("safe.txt", b"content")))

    assert raised.value.code == "workspace_extraction_failed"
    assert list(tmp_path.iterdir()) == []


def test_uuid_collision_does_not_remove_existing_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    existing_workspace = tmp_path / "collision"
    existing_workspace.mkdir()
    existing_file = existing_workspace / "keep.txt"
    existing_file.write_text("existing workspace", encoding="utf-8")
    monkeypatch.setattr(registry_module, "uuid4", lambda: SimpleNamespace(hex="collision"))
    registry = WorkspaceRegistry(tmp_path)

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(zip_bytes(("safe.txt", b"new upload")))

    assert raised.value.code == "workspace_extraction_failed"
    assert existing_file.read_text(encoding="utf-8") == "existing workspace"


def test_rejects_invalid_archive_without_leaking_host_paths(tmp_path: Path) -> None:
    registry = WorkspaceRegistry(tmp_path)

    with pytest.raises(ArchiveRejectedError) as raised:
        registry.create_from_zip(b"not a zip archive")

    assert raised.value.code == "invalid_archive"
    assert str(tmp_path) not in str(raised.value)
    assert list(tmp_path.iterdir()) == []


def test_rejects_archives_exceeding_count_or_size_limits(tmp_path: Path) -> None:
    too_many = WorkspaceRegistry(tmp_path / "many", limits=UploadLimits(max_files=1))
    too_large = WorkspaceRegistry(tmp_path / "large", limits=UploadLimits(max_uncompressed_bytes=3))
    too_compressed = WorkspaceRegistry(tmp_path / "compressed", limits=UploadLimits(max_compressed_bytes=1))
    archive = zip_bytes(("one.txt", b"abcd"), ("two.txt", b"efgh"))

    with pytest.raises(ArchiveRejectedError, match="too_many_files"):
        too_many.create_from_zip(archive)
    with pytest.raises(ArchiveRejectedError, match="archive_too_large"):
        too_large.create_from_zip(archive)
    with pytest.raises(ArchiveRejectedError, match="archive_too_large"):
        too_compressed.create_from_zip(archive)

    assert not (tmp_path / "many").exists() or list((tmp_path / "many").iterdir()) == []
    assert not (tmp_path / "large").exists() or list((tmp_path / "large").iterdir()) == []
    assert not (tmp_path / "compressed").exists() or list((tmp_path / "compressed").iterdir()) == []
