from tinytask.cli import main
from tinytask.storage import load_tasks


def test_add_then_list(capsys):
    assert main(["add", "buy", "milk"]) == 0
    assert main(["list"]) == 0
    out = capsys.readouterr().out
    assert "buy milk" in out


def test_done_hides_task_from_list(capsys):
    main(["add", "write report"])
    main(["done", "1"])
    capsys.readouterr()
    main(["list"])
    assert "write report" not in capsys.readouterr().out


def test_list_all_shows_done_tasks(capsys):
    main(["add", "water plants"])
    main(["done", "1"])
    capsys.readouterr()
    main(["list", "--all"])
    assert "[x] water plants" in capsys.readouterr().out


def test_search_finds_matching_title(capsys):
    main(["add", "call the bank"])
    main(["add", "walk the dog"])
    capsys.readouterr()
    main(["search", "bank"])
    out = capsys.readouterr().out
    assert "call the bank" in out
    assert "walk the dog" not in out


def test_done_unknown_id_fails():
    assert main(["done", "99"]) == 1


def test_add_rejects_bad_date(capsys):
    assert main(["add", "pay rent", "--due", "not-a-date"]) == 2
    assert load_tasks() == []
