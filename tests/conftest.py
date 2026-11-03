import pytest


@pytest.fixture(autouse=True)
def task_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setenv("TINYTASK_FILE", str(path))
    return path
