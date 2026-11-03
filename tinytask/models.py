"""The Task record and the helpers that read user input into it."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime

# Dates are documented as DD-MM-YYYY (see README).
DATE_FORMAT = "%m-%d-%Y"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    due: str | None = None  # stored as ISO YYYY-MM-DD
    created: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            done=bool(data.get("done", False)),
            due=data.get("due"),
            created=data.get("created", ""),
        )

    def is_overdue(self, today: date | None = None) -> bool:
        if self.done or not self.due:
            return False
        today = today or date.today()
        return date.fromisoformat(self.due) < today


def parse_due(text: str) -> str:
    """Turn a user-typed date (DD-MM-YYYY) into ISO YYYY-MM-DD."""
    parsed = datetime.strptime(text, DATE_FORMAT).date()
    return parsed.isoformat()
