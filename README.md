# tinytask

A tiny command-line to-do list. Your tasks live in one JSON file in your home
folder, so there is no account, no server and nothing to configure.

```console
$ tinytask add buy milk --due 07-11-2026
Added task 1: buy milk
$ tinytask add call the bank
Added task 2: call the bank
$ tinytask list
  1 [ ] buy milk  (due 2026-11-07)
  2 [ ] call the bank
$ tinytask done 1
Done: buy milk
```

## Install

You need Python 3.10 or newer.

```console
$ git clone https://github.com/TheRealJahaan/steward-demo
$ cd steward-demo
$ python3 -m pip install -e .
```

## Commands

| Command | What it does |
| --- | --- |
| `tinytask add <title> [--due DD-MM-YYYY]` | Add a task, optionally with a due date |
| `tinytask list [--all]` | Show open tasks, or every task with `--all` |
| `tinytask done <id>` | Mark a task finished |
| `tinytask remove <id>` | Delete a task |
| `tinytask search <text>` | Find tasks whose title contains the text |

Tasks are kept in `~/.tinytask.json`. Set `TINYTASK_FILE` to use another file.

## Project layout

- `tinytask/cli.py`: the commands and argument parsing
- `tinytask/models.py`: the `Task` record and date handling
- `tinytask/storage.py`: loading and saving the JSON file
- `tests/`: pytest tests, run with `python3 -m pytest`

## Contributing

New contributors are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), pick an
issue labelled `good first issue`, and ask in the project's Discord `#help`
channel if you get stuck.

## License

MIT
