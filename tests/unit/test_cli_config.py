"""What a login reads once: the chain, the file to edit, and the block that names it.

The file is the person's, and this command never writes it. So the test that matters is not that
the text looks right but that what it asks you to paste *is* the file it would then read -- valid
JSON, at the path this machine spelled, keeping the answers already there.
"""

import json
import textwrap

from office365 import cli

#: What ``_refuse`` answers: the command could not start, and exit 1 would say it ran and failed.
UNUSABLE = 2


def _home(tmp_path, answers=None):
    """A machine with this config file and no environment: the state a first run sees."""
    if answers is not None:
        (tmp_path / "config.json").write_text(json.dumps(answers), "utf-8")
    return tmp_path


def _clean(monkeypatch, home):
    for name in ("O365_CLIENT_ID", "O365_TENANT", "O365_SITE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("O365_HOME", str(home))


def test_what_the_file_answers_is_reported_with_the_file_that_answers_it(tmp_path, monkeypatch, capsys):
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com"})
    _clean(monkeypatch, home)

    assert cli.config([]) == 0

    out = capsys.readouterr().out
    assert "contoso.onmicrosoft.com" in out
    assert str(home / "config.json") in out
    assert cli.NOT_SET in out


def test_the_environment_wins_over_the_file(tmp_path, monkeypatch):
    home = _home(tmp_path, {"client_id": "from-the-file"})
    _clean(monkeypatch, home)
    monkeypatch.setenv("O365_CLIENT_ID", "from-the-shell")

    assert cli._resolved("client_id", cli._prefs()) == ("from-the-shell", "environment")


def test_the_advice_is_a_file_that_parses_and_keeps_what_is_already_answered(tmp_path, monkeypatch):
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com"})
    _clean(monkeypatch, home)

    advice = cli._advice(["client_id"])
    document = json.loads(textwrap.dedent(advice.split("<<'EOF'\n", 1)[1].split("EOF", 1)[0]))

    assert document == {"tenant": "contoso.onmicrosoft.com", "client_id": cli.EXAMPLES["client_id"]}
    assert str(home / "config.json") in advice


def test_one_setting_answers_the_value_a_command_would_use_and_exits_one_when_nothing_does(
    tmp_path, monkeypatch, capsys
):
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com"})
    _clean(monkeypatch, home)

    assert cli.config(["tenant"]) == 0
    assert capsys.readouterr().out.strip() == "contoso.onmicrosoft.com"

    assert cli.config(["client_id"]) == 1
    assert "no client id yet" in capsys.readouterr().err


def test_a_login_without_a_client_id_prints_the_file_to_write(tmp_path, monkeypatch, capsys):
    home = _home(tmp_path)
    _clean(monkeypatch, home)

    assert cli.main(["login"]) == UNUSABLE

    err = capsys.readouterr().err
    assert "no client id yet" in err
    assert f"cat > {home / 'config.json'} <<'EOF'" in err


def test_the_config_page_offers_the_keys_it_reports():
    words = [word for word, _ in cli._following(["config"], "")]

    assert words == [setting.key for setting in cli.SETTINGS]
