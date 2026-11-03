"""Reading and writing the task list. Everything lives in one JSON file."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .models import Task

DEFAULT_PATH = Path.home() / ".tinytask.json"


def store_path() -> Path:
    """The file tasks are kept in. TINYTASK_FILE overrides it (the tests use this)."""
    override = os.environ.get("TINYTASK_FILE")
    return Path(override) if override else DEFAULT_PATH


def load_tasks(path: Path | None = None) -> list[Task]:
    path = path or store_path()
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as fh:
        raw = json.load(fh)
    return [Task.from_dict(item) for item in raw]


def save_tasks(tasks: list[Task], path: Path | None = None) -> None:
    path = path or store_path()
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump([t.to_dict() for t in tasks], fh, indent=2)
    tmp.replace(path)


def next_id(tasks: list[Task]) -> int:
    return len(tasks) + 1
