from __future__ import annotations

import io
import stat
import zipfile
from pathlib import Path

import pytest

from safe_code_harness.workspaces.registry import WorkspaceRegistry
from safe_code_harness.workspaces.upload import ArchiveRejectedError, UploadLimits


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
        (".env", "protected_archive_path"),
        (".git/config", "protected_archive_path"),
        ("config/api_key.txt", "protected_archive_path"),
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
