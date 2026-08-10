from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_readme_contains_reproducible_run_and_key_safety_instructions() -> None:
    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")

    assert "docker pull" in readme
    assert "Credential Manager" in readme
    assert "已知限制" in readme
