"""The tinytask command line: add, list, done, remove and search."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .models import Task, parse_due
from .storage import load_tasks, next_id, save_tasks


def cmd_add(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    due = None
    if args.due:
        try:
            due = parse_due(args.due)
        except ValueError:
            print(f"Could not read the date {args.due!r}. Use DD-MM-YYYY.", file=sys.stderr)
            return 2
    task = Task(id=next_id(tasks), title=" ".join(args.title), due=due)
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {task.id}: {task.title}")
    return 0


def format_task(task: Task) -> str:
    box = "[x]" if task.done else "[ ]"
    due = f"  (due {task.due})" if task.due else ""
    return f"{task.id:>3} {box} {task.title}{due}"


def cmd_list(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    shown = [t for t in tasks if args.all or not t.done]
    if not shown:
        print("Nothing to do.")
        return 0
    for task in shown:
        print(format_task(task))
    return 0


def _find(tasks: list[Task], task_id: int) -> Task | None:
    return next((t for t in tasks if t.id == task_id), None)


def cmd_done(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    task = _find(tasks, args.id)
    if task is None:
        print(f"No task with id {args.id}.", file=sys.stderr)
        return 1
    task.done = True
    save_tasks(tasks)
    print(f"Done: {task.title}")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    tasks = load_tasks()
    task = _find(tasks, args.id)
    if task is None:
        print(f"No task with id {args.id}.", file=sys.stderr)
        return 1
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Removed: {task.title}")
    return 0


def search(tasks: list[Task], text: str) -> list[Task]:
    return [t for t in tasks if text in t.title]


def cmd_search(args: argparse.Namespace) -> int:
    found = search(load_tasks(), args.text)
    if not found:
        print("No matches.")
        return 0
    for task in found:
        print(format_task(task))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tinytask", description="A tiny to-do list.")
    parser.add_argument("--version", action="version", version=f"tinytask {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", nargs="+", help="what to do")
    add.add_argument("--due", help="due date, DD-MM-YYYY")
    add.set_defaults(func=cmd_add)

    lst = sub.add_parser("list", help="show open tasks")
    lst.add_argument("--all", action="store_true", help="include finished tasks")
    lst.set_defaults(func=cmd_list)

    done = sub.add_parser("done", help="mark a task finished")
    done.add_argument("id", type=int)
    done.set_defaults(func=cmd_done)

    rm = sub.add_parser("remove", help="delete a task")
    rm.add_argument("id", type=int)
    rm.set_defaults(func=cmd_remove)

    srch = sub.add_parser("search", help="find tasks by words in the title")
    srch.add_argument("text")
    srch.set_defaults(func=cmd_search)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
