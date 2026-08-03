def test_package_exposes_version() -> None:
    from safe_code_harness import __version__

    assert __version__ == "0.1.0"
