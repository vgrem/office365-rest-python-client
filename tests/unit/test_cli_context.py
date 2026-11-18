"""A SharePoint session is addressed at one site collection, and the command line says which.

The boundary is the model's: ``ClientContext(base_url)`` is one site, ``client.tenant`` is the
tenant holding them, and the token is one for all of them. So the store keeps the sites a
session has been pointed at, ``use`` moves the boundary, ``--site`` moves it for one command,
and a sentence that could cost something -- the ``--yes`` refusal, ``--dry-run``'s URL -- names
the site it would reach.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from office365.cli import _address, _current, _remember, _site_of, _summary, context, main, use

SITE = "https://contoso.sharepoint.com/sites/finance"
OTHER = "https://contoso.sharepoint.com/sites/hr"
REFUSED = 2


@pytest.fixture
def store(tmp_path, monkeypatch: pytest.MonkeyPatch) -> "dict":
    """A session store of this test's own, holding one SharePoint session mid-site."""
    path = tmp_path / "sessions.json"
    monkeypatch.setenv("O365_HOME", str(tmp_path))
    kept = {
        "sharepoint": {
            "mode": "device-flow",
            "method": "with_device_flow",
            "client_id": "an-app",
            "constructor": {"base_url": SITE},
            "claims": {"preferred_username": "oleg@contoso.com", "tid": "a-tenant"},
            "token": {"access_token": "live", "expires_on": 0},
            "cache": "",
        }
    }
    path.write_text(json.dumps(kept), "utf-8")
    return kept


class _Web:
    """The site's one web, read for its title -- the one request a `use` sends."""

    def __init__(self, title: str = "Finance") -> None:
        self.title = title

    def get(self) -> "_Web":
        return self

    def select(self, names) -> "_Web":
        self.selected = list(names)
        return self

    def execute_query(self) -> "_Web":
        return self


class _Client:
    def __init__(self, title: str = "Finance", fail: "Exception | None" = None) -> None:
        self.web = _Web(title)
        self.fail = fail


def _stub_client(monkeypatch: pytest.MonkeyPatch, client: "_Client") -> "list[dict]":
    """Answer `_client` with a stub, and record the site each call asked for."""
    asked: "list[dict]" = []

    def fake(audience: str, live: bool = True, site: "str | None" = None):
        asked.append({"audience": audience, "live": live, "site": site})
        if client.fail is not None:
            raise client.fail
        return client

    monkeypatch.setattr("office365.cli._client", fake)
    return asked


def test_a_bare_name_means_the_site_of_that_name_under_the_known_host(store: "dict") -> None:
    entry = store["sharepoint"]

    assert _address("sharepoint", entry, "hr") == OTHER
    assert _address("sharepoint", entry, "sites/service") == "https://contoso.sharepoint.com/sites/service"
    assert (
        _address("sharepoint", entry, "https://other.sharepoint.com/sites/x") == "https://other.sharepoint.com/sites/x"
    )


def test_a_remembered_site_answers_by_its_title_as_well_as_its_name(store: "dict") -> None:
    entry = _remember(store["sharepoint"], OTHER, "Human Resources")

    assert _address("sharepoint", entry, "hr") == OTHER
    assert _address("sharepoint", entry, "human resources") == OTHER


def test_a_name_with_no_known_host_is_refused_rather_than_guessed(store: "dict") -> None:
    entry = {**store["sharepoint"], "constructor": {}, "current": ""}

    with pytest.raises(LookupError, match="pass a full URL"):
        _address("sharepoint", entry, "hr")


def test_use_reads_the_site_then_remembers_it(store: "dict", monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    asked = _stub_client(monkeypatch, _Client(title="Human Resources"))

    assert use("sharepoint", ["hr"]) == 0
    assert asked[0]["site"] == OTHER  # the one request went to the site being chosen
    assert capsys.readouterr().out.strip() == "context: contoso.sharepoint.com/sites/hr — Human Resources"

    kept = json.loads((Path(os.environ["O365_HOME"]) / "sessions.json").read_text())
    entry = kept["sharepoint"]
    assert entry["current"] == OTHER
    assert entry["contexts"][0] == {"url": OTHER, "title": "Human Resources"}
    assert entry["contexts"][1]["url"] == SITE  # the old site is remembered, not forgotten


def test_a_site_that_does_not_answer_is_not_current(store: "dict", monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    _stub_client(monkeypatch, _Client(fail=RuntimeError("404, Site not found")))

    assert use("sharepoint", ["hr"]) == REFUSED
    assert "Site not found" in capsys.readouterr().err
    assert _current("sharepoint", store["sharepoint"]) == SITE  # the store is untouched


def test_use_with_no_session_says_which_login_to_run(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setenv("O365_HOME", "/nonexistent-o365-home")

    assert use("sharepoint", ["hr"]) == REFUSED
    assert "o365 sharepoint login" in capsys.readouterr().err


def test_context_reads_the_store_and_sends_nothing(store: "dict", monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    def no_request(*args, **kwargs):
        raise AssertionError("`context` must not need the service")

    monkeypatch.setattr("office365.cli._client", no_request)

    assert context("sharepoint") == 0
    printed = capsys.readouterr().out

    assert "at contoso.sharepoint.com/sites/finance" in printed
    assert "another site: o365 sharepoint use <url>" in printed


def test_the_summary_names_the_site_and_its_title(store: "dict") -> None:
    entry = _remember(store["sharepoint"], OTHER, "Human Resources")

    assert "at contoso.sharepoint.com/sites/hr — Human Resources" in _summary("sharepoint", entry)


def test_the_refusal_names_the_site_a_delete_would_reach(store: "dict", monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    assert main(["sharepoint", "web", "delete"]) == REFUSED
    printed = capsys.readouterr().err

    assert "`delete` on contoso.sharepoint.com/sites/finance destroys" in printed


def test_a_dry_run_shows_the_full_address_of_the_chosen_site(
    store: "dict", monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    # The address is the boundary, so the preview prints all of it -- scheme, host and path.
    assert main(["sharepoint", "web", "get", "--dry-run", "--site", "hr"]) == 0
    assert capsys.readouterr().out.splitlines()[0] == (f"GET {OTHER}/_api/Web?$select=Title,Url,ServerRelativeUrl")


def test_site_of_answers_a_word_it_can_and_the_word_itself_otherwise(store: "dict") -> None:
    assert _site_of("sharepoint") == "contoso.sharepoint.com/sites/finance"
    assert _site_of("sharepoint", "hr") == "contoso.sharepoint.com/sites/hr"
    # A typo is still named, rather than a sentence losing the site it is about.
    assert _site_of("sharepoint", "https://x.sharepoint.com/sites/none") == "x.sharepoint.com/sites/none"


def test_arguments_carry_the_site_scoped_flags() -> None:
    # Pinned as a shape: `--site` is only declared where a root is addressed at one site.
    from office365.cli import _flag_words
    from office365.routing import route

    words = dict(_flag_words(route("sharepoint", "web", "get")))
    assert "--site" in words

    words = dict(_flag_words(route("directory", "user", "get")))
    assert "--site" not in words
