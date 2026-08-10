from pathlib import Path

from safe_code_harness.governance.path_sandbox import PathSandbox
from safe_code_harness.tools.file_tools import FileTools


def test_file_tools_read_and_write_a_sandboxed_file(tmp_path: Path) -> None:
    tools = FileTools(PathSandbox(tmp_path))

    written = tools.write("src/main.py", "print('safe')\n")
    read = tools.read("src/main.py")

    assert written.ok is True
    assert read.ok is True
    assert read.details == "print('safe')\n"
    assert read.artifacts == (str(tmp_path / "src" / "main.py"),)


def test_file_tools_do_not_access_a_path_outside_the_sandbox(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    tools = FileTools(PathSandbox(tmp_path))

    result = tools.write("../outside.txt", "must not escape")

    assert result.ok is False
    assert result.summary == "file write failed"
    assert outside.exists() is False
