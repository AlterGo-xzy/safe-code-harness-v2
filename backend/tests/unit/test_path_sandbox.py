from pathlib import Path

import pytest

from safe_code_harness.governance.path_sandbox import PathSandbox


def test_sandbox_resolves_a_path_inside_the_workspace(tmp_path: Path) -> None:
    assert PathSandbox(tmp_path).resolve("src/main.py") == tmp_path / "src" / "main.py"


def test_sandbox_blocks_workspace_escape(tmp_path: Path) -> None:
    with pytest.raises(PermissionError, match="workspace escape"):
        PathSandbox(tmp_path).resolve("../secret.txt")


@pytest.mark.parametrize("path", [".env", ".git/config", "secrets/token.txt"])
def test_sandbox_blocks_sensitive_workspace_paths(tmp_path: Path, path: str) -> None:
    with pytest.raises(PermissionError, match="blocked sensitive path"):
        PathSandbox(tmp_path).resolve(path)
