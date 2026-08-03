from pathlib import Path
import os
import subprocess

import pytest

from safe_code_harness.governance.path_sandbox import PathSandbox


def test_sandbox_resolves_a_path_inside_the_workspace(tmp_path: Path) -> None:
    assert PathSandbox(tmp_path).resolve("src/main.py") == tmp_path / "src" / "main.py"


def test_sandbox_blocks_workspace_escape(tmp_path: Path) -> None:
    with pytest.raises(PermissionError, match="workspace escape"):
        PathSandbox(tmp_path).resolve("../secret.txt")


@pytest.mark.parametrize(
    "path",
    [
        ".env",
        ".env.local",
        "nested/.env.production",
        ".GIT/config",
        "nested/SECRETS/token.txt",
    ],
)
def test_sandbox_blocks_sensitive_workspace_paths(tmp_path: Path, path: str) -> None:
    with pytest.raises(PermissionError, match="blocked sensitive path"):
        PathSandbox(tmp_path).resolve(path)


def test_sandbox_blocks_a_symlink_that_resolves_to_a_sensitive_path(tmp_path: Path) -> None:
    sensitive_directory = tmp_path / ".env.production"
    sensitive_directory.mkdir()
    link = tmp_path / "linked-config"
    if os.name == "nt":
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(sensitive_directory)],
            check=True,
            capture_output=True,
            text=True,
        )
    else:
        link.symlink_to(sensitive_directory, target_is_directory=True)

    with pytest.raises(PermissionError, match="blocked sensitive path"):
        PathSandbox(tmp_path).resolve(link / "settings.json")
