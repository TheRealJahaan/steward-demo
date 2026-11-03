from tinytask.models import Task
from tinytask.storage import load_tasks, save_tasks


def test_missing_file_means_no_tasks():
    assert load_tasks() == []


def test_round_trip():
    tasks = [Task(id=1, title="one"), Task(id=2, title="two", done=True)]
    save_tasks(tasks)
    loaded = load_tasks()
    assert [t.title for t in loaded] == ["one", "two"]
    assert loaded[1].done is True
