"""What ``o365 doctor`` says before the first command, and what it refuses to guess.

The page has two halves and each is answered from something already committed: the product block
is the index, and a route's marks are the declaration joined to the token's own ``scp``/``roles``.
Neither sends a request to the endpoint being asked about, which is the claim these tests pin -
so the two reads that do need a tenant (the subscriptions and the directory roles) are patched
here rather than imitated, and ``test_licence_report`` keeps ownership of what a licence answer
means.
"""

from __future__ import annotations

import base64
import json
import time
from typing import Any

import pytest
from office365 import cli
from office365.permissions.declaration import TENANT

#: Where a Graph requirement's names are a grant: the audience a token must have been issued for.
GRAPHS = "https://graph.microsoft.com"

#: What a refused word answers the shell with, so a typo is not mistaken for a report.
REFUSED = 2


def _jwt(**claims: Any) -> str:
    """A token whose payload carries ``claims``; the signature is never read."""
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return f"e30.{payload}.sig"


def _store(monkeypatch: pytest.MonkeyPatch, tmp_path: Any, **sessions: Any) -> None:
    """Put these sessions where ``O365_HOME`` points, so no test reads the real store."""
    monkeypatch.setenv("O365_HOME", str(tmp_path))
    (tmp_path / "sessions.json").write_text(json.dumps(sessions), "utf-8")


def test_the_page_ignores_a_route_it_cannot_mark_and_says_why(monkeypatch, tmp_path, capsys) -> None:
    """No session is a sentence, not an exit: the product block still answers."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_live_graph", lambda: pytest.fail("no session means no client"))

    assert cli.main(["doctor"]) == 0

    printed = capsys.readouterr().out
    assert printed.startswith("doctor: attention — no session; run o365 login")
    assert "PRODUCT" in printed
    assert "intune" in printed


def test_a_route_marks_the_licence_the_type_declares_a_call_needs(monkeypatch, tmp_path, capsys) -> None:
    """``retire`` names INTUNE_A on the type; the doctor answers with the tenant, not with the call."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_live_graph", lambda: None)
    monkeypatch.setattr(cli, "_held_plans", lambda client: frozenset({"INTUNE_A"}))

    assert cli.main(["doctor", "intune", "managed-device", "retire"]) == 0

    printed = capsys.readouterr().out
    assert "INTUNE_A" in printed
    assert "have" in printed


def test_a_route_marks_the_grant_the_token_carries_and_not_the_one_it_lacks(monkeypatch, tmp_path, capsys) -> None:
    """A user's token answers the delegated flow and cannot answer the application one."""
    _store(
        monkeypatch,
        tmp_path,
        graph={
            "mode": "device-flow",
            "constructor": {},
            "token": {"access_token": _jwt(aud=GRAPHS, scp="User.ReadWrite.All")},
        },
    )
    monkeypatch.setattr(cli, "_live_graph", lambda: None)

    assert cli.main(["doctor", "directory", "user", "delete"]) == 0

    printed = capsys.readouterr().out
    assert "delegated" in printed and "have" in printed
    assert "application" in printed and "unknown" in printed
    assert "unknown is not missing" in printed


def test_a_call_the_model_does_not_describe_is_reported_not_refused(monkeypatch, tmp_path, capsys) -> None:
    _store(monkeypatch, tmp_path)

    assert cli.main(["doctor", "intune", "managed-device", "list"]) == 0

    assert "declares no permission" in capsys.readouterr().out


def test_a_word_that_names_no_route_is_refused_with_the_close_matches(monkeypatch, tmp_path, capsys) -> None:
    _store(monkeypatch, tmp_path)

    assert cli.main(["doctor", "intune", "managed-devicez"]) == REFUSED

    assert "did you mean managed-device" in capsys.readouterr().err


def _facts(**changed: Any) -> "dict[str, Any]":
    """What the two tenant reads answer, so a test about the page sends none of them."""
    return {
        "tenant": "contoso.onmicrosoft.com",
        "held": frozenset({"INTUNE_A"}),
        "assigned": frozenset(),
        "roles": ("Global Administrator",),
        "why": "",
        **changed,
    }


def test_the_page_names_only_the_products_that_name_a_licence(monkeypatch, tmp_path, capsys) -> None:
    """Twenty products stamp no licence: one sentence, because twenty rows of zeroes say it worse."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_tenant_facts", _facts)

    assert cli.main(["doctor"]) == 0

    printed = capsys.readouterr().out
    assert "LICENSED" in printed and "booking" not in printed
    assert "no licence is named under the other" in printed
    assert "roles: 1 held — Global Administrator" in printed


def test_wide_restores_the_row_a_table_would_have_to_shorten(monkeypatch, tmp_path, capsys) -> None:
    """The families a plan opens, and every product: the report behind the page."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_tenant_facts", _facts)

    assert cli.main(["doctor", "-o", "wide"]) == 0

    printed = capsys.readouterr().out
    assert "FAMILIES" in printed and "intune.devices" in printed
    assert "booking" in printed
    assert "no licence is named under" not in printed


def test_the_verdict_says_attention_and_names_the_command_that_fixes_an_expired_token() -> None:
    """The first line, because the expired token is the reason a reader opened the page."""
    sessions = {"sharepoint": {"mode": "device-flow", "claims": {"exp": int(time.time()) - 60}}}

    line = cli._verdict(sessions, {"why": "", "roles": ("Global Administrator",)}, [])

    assert line == "doctor: attention — the sharepoint session expired; run o365 sharepoint login"


def test_the_verdict_counts_what_it_can_and_calls_a_failed_read_unread() -> None:
    """``unknown`` is not ``no``: a licence that could not be read is not a licence the tenant lacks."""
    sessions = {"graph": {"mode": "device-flow", "claims": {"exp": int(time.time()) + 600}}}
    facts = {"why": "the tenant's subscriptions could not be read: is Licence.Read.All granted?", "roles": None}

    assert cli._verdict(sessions, facts, []) == (
        "doctor: unread — the tenant's subscriptions could not be read: is Licence.Read.All granted?"
    )


def test_the_verdict_says_ok_with_the_three_numbers_it_read() -> None:
    sessions = {"graph": {"mode": "device-flow", "claims": {"exp": int(time.time()) + 600}}}
    records = [{"held": "yes"}, {"held": "no"}]

    assert cli._verdict(sessions, {"why": "", "roles": ("A", "B")}, records) == (
        "doctor: ok — 1 session, 1 of 2 licences, 2 roles"
    )


def test_a_product_page_counts_its_nouns_and_names_what_the_missing_ones_take(monkeypatch, tmp_path, capsys) -> None:
    """Six nouns waiting on one scope are one row: the name to grant, not the wall it unblocks."""
    _store(
        monkeypatch,
        tmp_path,
        graph={
            "mode": "device-flow",
            "constructor": {},
            "token": {"access_token": _jwt(aud=GRAPHS, scp="User.Read")},
        },
    )
    monkeypatch.setattr(cli, "_live_graph", lambda: pytest.fail("outlook names no licence and no role"))

    assert cli.main(["doctor", "outlook"]) == 0

    printed = capsys.readouterr().out
    assert "37 nouns" in printed and "RESULT" in printed
    assert printed.count("Place.Read.All") == 1
    assert "PERMISSION" not in printed


def test_wide_is_one_row_per_noun_with_every_gate_it_declares(monkeypatch, tmp_path, capsys) -> None:
    """The matrix behind the page: a noun nobody needed to mention is still answerable."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_live_graph", lambda: pytest.fail("outlook names no licence and no role"))

    assert cli.main(["doctor", "outlook", "-o", "wide"]) == 0

    printed = capsys.readouterr().out
    assert "NOUN" in printed and "check-in-claim" in printed
    assert "unmarked" in printed


def test_a_noun_nobody_stamped_is_unmarked_and_never_counted_as_held() -> None:
    """Nothing was judged on a type with no marker; calling that ``have`` would be a claim, not a read."""
    gates = cli.Gates(claims=None, held=frozenset(), assigned=frozenset(), roles=(), why="")

    row = cli._statement_row(cli.Statement("thing", (), TENANT, (), ()), gates)

    assert row["result"] == cli.UNMARKED


def test_an_unread_licence_is_unknown_and_an_absent_one_is_missing() -> None:
    """The same noun, twice: a tenant that could not be asked is not a tenant that said no."""
    statement = cli.Statement("managed-device", ("INTUNE_A",), TENANT, (), ())

    unread = cli._statement_row(statement, cli.Gates(None, None, None, (), "could not be read"))
    absent = cli._statement_row(statement, cli.Gates(None, frozenset(), frozenset(), (), ""))

    assert unread["result"] == "unknown"
    assert absent["result"] == "missing"
    assert absent["needs"] == "licence INTUNE_A"
