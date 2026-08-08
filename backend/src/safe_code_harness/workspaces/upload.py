from __future__ import annotations

import io
import re
import shutil
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from safe_code_harness.governance.path_sandbox import PathSandbox


_DRIVE_PATH = re.compile(r"^[A-Za-z]:")
_SECRET_NAME = re.compile(r"(?:api[-_]?key|secret|token|password|credential)", re.IGNORECASE)
_PROTECTED_PARTS = frozenset(
    {".env", ".git", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist"}
)
_WINDOWS_DEVICE_STEMS = frozenset(
    {"con", "prn", "aux", "nul", *(f"com{number}" for number in range(1, 10)), *(f"lpt{number}" for number in range(1, 10))}
)


@dataclass(frozen=True)
class UploadLimits:
    max_archive_bytes: int = 8 * 1024 * 1024
    max_files: int = 500
    max_compressed_bytes: int = 8 * 1024 * 1024
    max_uncompressed_bytes: int = 20 * 1024 * 1024


class ArchiveRejectedError(ValueError):
    """A safe, stable archive rejection reason for the API boundary."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def extract_verified_zip(data: bytes, destination: Path, limits: UploadLimits) -> int:
    """Validate every member before writing any archive content to *destination*."""

    if len(data) > limits.max_archive_bytes:
        raise ArchiveRejectedError("archive_too_large")

    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except (zipfile.BadZipFile, OSError) as exc:
        raise ArchiveRejectedError("invalid_archive") from exc

    try:
        members = archive.infolist()
        files = [member for member in members if not member.is_dir()]
        _validate_members(members, files, limits)

        sandbox = PathSandbox(destination)
        destination.mkdir(parents=True, exist_ok=False)
        try:
            for member in files:
                target = sandbox.resolve(_member_path(member.filename))
                target.parent.mkdir(parents=True, exist_ok=True)
                _copy_member_with_limit(archive, member, target, limits.max_uncompressed_bytes)
        except ArchiveRejectedError:
            shutil.rmtree(destination, ignore_errors=True)
            raise
        except Exception as exc:
            shutil.rmtree(destination, ignore_errors=True)
            raise ArchiveRejectedError("workspace_extraction_failed") from exc
        return len(files)
    finally:
        archive.close()


def _validate_members(
    members: list[zipfile.ZipInfo], files: list[zipfile.ZipInfo], limits: UploadLimits
) -> None:
    if not files:
        raise ArchiveRejectedError("empty_archive")
    if len(members) > limits.max_files:
        raise ArchiveRejectedError("too_many_files")

    compressed_size = 0
    uncompressed_size = 0
    target_paths: set[PurePosixPath] = set()
    for member in members:
        relative = _member_path(member.filename)
        if _is_symlink(member):
            raise ArchiveRejectedError("unsafe_archive_member")
        _validate_member_path(relative)
        if member.is_dir():
            continue
        if relative in target_paths:
            raise ArchiveRejectedError("duplicate_archive_member")
        target_paths.add(relative)
        compressed_size += member.compress_size
        uncompressed_size += member.file_size
        if compressed_size > limits.max_compressed_bytes or uncompressed_size > limits.max_uncompressed_bytes:
            raise ArchiveRejectedError("archive_too_large")


def _member_path(name: str) -> PurePosixPath:
    normalized = name.replace("\\", "/")
    if "\x00" in normalized or normalized.startswith("//") or _DRIVE_PATH.match(normalized):
        raise ArchiveRejectedError("unsafe_archive_path")
    path = PurePosixPath(normalized)
    if (
        path.is_absolute()
        or ".." in path.parts
        or not path.parts
        or any(_is_windows_ambiguous(part) or ":" in part for part in path.parts)
    ):
        raise ArchiveRejectedError("unsafe_archive_path")
    return path


def _is_windows_ambiguous(part: str) -> bool:
    return part.endswith((".", " ")) or part.split(".", 1)[0].lower() in _WINDOWS_DEVICE_STEMS


def _validate_member_path(path: PurePosixPath) -> None:
    for part in path.parts:
        lowered = part.lower()
        if lowered in _PROTECTED_PARTS or _SECRET_NAME.search(lowered):
            raise ArchiveRejectedError("protected_archive_path")


def _is_symlink(member: zipfile.ZipInfo) -> bool:
    return stat.S_IFMT(member.external_attr >> 16) == stat.S_IFLNK


def _copy_member_with_limit(
    archive: zipfile.ZipFile, member: zipfile.ZipInfo, target: Path, byte_limit: int
) -> None:
    copied = 0
    with archive.open(member) as source, target.open("xb") as destination:
        while chunk := source.read(64 * 1024):
            copied += len(chunk)
            if copied > byte_limit:
                raise ArchiveRejectedError("archive_too_large")
            destination.write(chunk)
