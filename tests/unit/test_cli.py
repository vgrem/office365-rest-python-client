"""The command line: the words it is offered, the walk behind them, and its two pages.

Nothing here is hand-written for the CLI to read. A route is drawn from the getters, a command
from the stamps on its method, a licence from the type's marker, a format from what the command
accepts — so a test asserts what the model says, and a command that disagrees is the defect.

The model layer keeps its own small tests (``test_verbs``, ``test_hints``, ``test_render``); this
file owns the command: the walk, what it prints, what a shell is offered, what a login says, the
config file, and the two pages ``doctor`` and ``licences`` print.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import textwrap
import time
from typing import Any

import pytest
from office365 import cli, completion
from office365.cli import _feed, _following, _keyed, _rows, _walk
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.licensing.report import NO, UNKNOWN, YES, area_of, headline, of, products, rows
from office365.migration.offline import offline_context
from office365.permissions.declaration import TENANT, USER
from office365.routing import _links, chain, route
from office365.routing import products as published
from office365.runtime.client_object import ClientObject
from office365.runtime.client_object_collection import ClientObjectCollection

#: What ``_refuse`` answers: the command could not start, and exit 1 would say it ran and failed.
REFUSED = 2

#: Where a Graph requirement's names are a grant: the audience a token must have been issued for.
GRAPHS = "https://graph.microsoft.com"


# --- the vocabulary ----------------------------------------------------------------


class Widget(ClientObject):
    pass


class Cabinet(ClientObject):
    @property
    def widget(self) -> Widget | None:
        return Widget(self.context)

    @property
    def spare(self) -> "Widget | None":
        return None


def test_a_route_is_drawn_from_the_getters_so_it_exists_before_a_token_does() -> None:
    # The two spellings of "this, or nothing" are one edge: a route the model draws must not
    # disappear because the declaration said ``Optional[X]``.
    assert _links(Cabinet)["widget"] is Widget
    assert chain(Cabinet, Widget) == ("widget",)
    # A product is a package that does not say it is not one.
    assert "directory" in published() and "runtime" not in published()


# --- the walk ----------------------------------------------------------------------


def test_a_list_walks_to_the_feed_and_a_feed_that_hangs_off_one_item_is_refused() -> None:
    # ``list`` is ``get()`` on the feed, not on an item: ``Message`` is not reachable from the
    # root, and ``User`` is reachable through ``me`` — which would print the caller as the list.
    assert _walk(GraphClient, route("outlook", "message", "list")) == ("me", "messages")
    assert _walk(GraphClient, route("directory", "user", "list")) == ("users",)
    assert _walk(GraphClient, route("intune", "managed-device", "list")) == ("device_management", "managed_devices")
    # ``attachments`` hangs off one ``Message``: no link from the root names its key.
    assert _walk(GraphClient, route("outlook", "message", "attachments", "list")) is None
    assert _walk(GraphClient, route("onedrive", "drive", "get")) == ("me", "drive")


def test_a_key_names_the_item_the_verb_acts_on() -> None:
    """``user delete --id <upn>`` deletes that user: the feed the noun states, indexed by the key."""
    found = route("directory", "user", "delete")
    assert _keyed(found, getattr(found.here, found.method))
    assert _feed(GraphClient, found, "directory") == ("users",)

    # A feed reached through one item takes that item's key.
    attachments = route("outlook", "message", "attachments", "list")
    assert _feed(GraphClient, attachments, "outlook") == ("me", "messages")

    # A create has no item for a key to name.
    create = route("directory", "user", "create")
    assert _keyed(create, getattr(create.here, create.method)) is False


def test_a_key_is_what_the_dry_run_prints(monkeypatch, capsys) -> None:
    """Nothing is sent, so the client needs no token: the URL is asked of the model."""
    monkeypatch.setattr(cli, "_client", lambda *word, **rest: GraphClient())
    assert cli.command("directory", ["user", "delete"], ["--id", "a.dyukov@contoso.com", "-n", "--yes"]) == 0
    assert capsys.readouterr().out.strip() == "DELETE https://graph.microsoft.com/v1.0/users/a.dyukov@contoso.com"


def test_the_refusal_offers_a_key_only_where_it_would_work(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "_client", lambda *word, **rest: GraphClient())

    assert cli.command("outlook", ["message", "attachments", "list"], []) == REFUSED
    assert capsys.readouterr().err.rstrip().endswith("; --id names it")

    # A noun with no feed is not offered a flag the command does not declare.
    assert cli.command("directory", ["administrative-unit", "get"], []) == REFUSED
    assert "--id" not in capsys.readouterr().err


# --- what a command prints ---------------------------------------------------------


def _items(*names: str) -> ClientObjectCollection:
    feed = ClientObjectCollection(offline_context(), User, None)
    for name in names:
        item = User(offline_context())
        item.set_property("displayName", name)
        feed.add_child(item)
    return feed


def test_a_feed_is_one_row_per_item_and_an_empty_feed_is_no_rows() -> None:
    """An empty feed must not become a row: the envelope is not a device."""
    assert [row.display_name for row in _rows(_items("a", "b"))] == ["a", "b"]
    assert _rows(_items()) == []


# --- what a shell is offered -------------------------------------------------------


@pytest.fixture(autouse=True)
def _private_cache(tmp_path, monkeypatch):
    """Keep the developer's own completion cache, and an earlier test's, out of the test."""
    monkeypatch.setenv("O365_CACHE", str(tmp_path / "completion.json"))
    completion._document.cache_clear()


def test_a_noun_answers_its_commands_before_its_links_and_every_word_routes() -> None:
    node = completion.following("outlook", ("message",))
    assert node is not None
    kinds = [candidate.kind for candidate in node]

    assert kinds[0] == "action"
    assert kinds[kinds.index("navigation") - 1] == "action"
    assert {"delete", "attachments"} <= {candidate.word for candidate in node}
    assert len({candidate.word for candidate in node}) == len(node)
    assert all(route("outlook", "message", candidate.word) is not None for candidate in node)
    # A line that ends on an action answers nothing: the flags there are a signature.
    assert completion.following("outlook", ("message", "delete")) is None


def test_a_warm_node_is_served_from_the_cache_and_rebuilt_only_when_a_module_changes(monkeypatch) -> None:
    completion.warm(["outlook"])
    monkeypatch.setattr(completion, "_build", lambda product, path: pytest.fail(f"built {product} {path}"))
    assert completion.following("outlook", ("message",))

    built: list = []
    monkeypatch.setattr(completion, "_build", lambda product, path: built.append(path) or ())
    completion.following("outlook", ("message",))
    assert built == []  # the second TAB does not ask the model again

    document = json.loads(completion.cache_path().read_text("utf-8"))
    document["stamps"]["outlook"] = {"office365/outlook/mail/messages/message.py": 1}
    completion.cache_path().write_text(json.dumps(document), "utf-8")
    completion._document.cache_clear()  # forget this process's copy, as the next TAB would be
    completion.following("outlook", ("message",))
    assert built == [("message",)]


def test_a_command_offers_only_the_formats_it_accepts_and_the_words_it_owns() -> None:
    """A TAB that answered ``csv`` for ``doctor`` would hand back a word argparse refuses."""
    assert [word for word, _ in _following(["doctor", "-o"], "")] == list(cli.DOCTOR_FORMATS)
    assert [word for word, _ in _following(["licences", "-o"], "")] == list(cli.LICENCE_FORMATS)
    # Level-0 answers what the command line owns before it asks the model.
    assert set(cli.SESSION) <= {word for word, _ in _following([], "")}
    assert [word for word, _ in _following(["config"], "")] == [setting.key for setting in cli.SETTINGS]
    assert _following(["nonsense"], "") == []


def test_the_script_asks_the_hidden_command_and_no_user_facing_word() -> None:
    written = completion.script("bash")

    assert "__complete" in written and "--prefix" in written
    with pytest.raises(LookupError, match="no completion script for 'tcsh'"):
        completion.script("tcsh")


CHILD = textwrap.dedent(
    """
    import json, sys
    from office365.cli import _served

    line = _served("graph")
    imported = sorted({name.split(".")[1] for name in sys.modules if name.startswith("office365.")})
    print(json.dumps({"line": line, "imported": imported}))
    """
)

#: ``doctor`` answers for the whole library, so it names every product and imports none. The
#: report module is imported before the snapshot because it is the page's own vocabulary.
DOCTOR = textwrap.dedent(
    """
    import contextlib, io, json, sys
    from office365.cli import main
    from office365.licensing.report import of  # noqa: F401 - the doctor's own vocabulary

    before = set(sys.modules)
    with contextlib.redirect_stdout(io.StringIO()):
        code = main(["doctor", "-o", "json"])
    imported = sorted({name.split(".")[1] for name in set(sys.modules) - before if name.startswith("office365.")})
    print(json.dumps({"code": code, "imported": imported}))
    """
)


def test_the_product_list_and_the_doctor_page_import_no_product(tmp_path) -> None:
    """The index is a file: 4 ms to parse, against 5.2 s to import the tree."""
    served = published()

    answer = json.loads(subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, check=True).stdout)
    assert not [name for name in answer["imported"] if name in served]
    assert answer["line"] == f"graph serves {len([n for n in served if n not in cli.AUDIENCES])} products: " + ", ".join(
        name for name in served if name not in cli.AUDIENCES
    )

    doctor = json.loads(
        subprocess.run(
            [sys.executable, "-c", DOCTOR],
            capture_output=True,
            text=True,
            check=True,
            env={**os.environ, "O365_HOME": str(tmp_path)},
        ).stdout
    )
    assert doctor["code"] == 0
    assert not [name for name in doctor["imported"] if name in served]


# --- what a login says -------------------------------------------------------------


def _entry(grants="Mail.Read Write User.Read", **claims):
    return {
        "mode": "device-flow",
        "claims": {
            "preferred_username": "vadimadm@mediadev8.onmicrosoft.com",
            "tid": "af6a80a4-8b4b-4879-88af-42ff8a545211",
            "scp": grants,
            "exp": int(time.time()) + 3900,
            **claims,
        },
    }


def test_a_login_counts_the_grants_and_a_report_names_them() -> None:
    welcome = cli._welcome("graph", _entry())

    assert "logged in: graph as vadimadm@mediadev8.onmicrosoft.com" in welcome
    assert "3 permissions" in welcome
    assert "Mail.Read" not in welcome  # the moment you signed in is not when you read 70 scopes
    assert "o365 whoami" in welcome and "o365 doctor" in welcome

    summary = cli._summary("graph", _entry())
    assert "grants: Mail.Read Write User.Read" in summary
    assert "mode device-flow, 1 h left" in summary


def test_a_token_with_no_scope_says_so_and_an_expired_one_says_how_long_ago() -> None:
    assert "no permissions" in cli._welcome("exchange", _entry(grants=""))

    # The fact belongs to the row, the command to the verdict: said twice it reads as two faults.
    summary = cli._summary("graph", _entry(exp=int(time.time()) - 60))
    assert "expired 1 min ago" in summary
    assert "fetching" not in summary and "run o365" not in summary
    # A session left for a week is not 10080 minutes.
    stale = _entry(exp=int(time.time()) - 3 * 24 * 3600 - 60)
    assert "expired 3 d ago" in cli._summary("graph", stale)


# --- the config file ---------------------------------------------------------------


def _home(tmp_path, answers=None):
    """A machine with this config file and no environment: the state a first run sees."""
    if answers is not None:
        (tmp_path / "config.json").write_text(json.dumps(answers), "utf-8")
    return tmp_path


def _clean(monkeypatch, home):
    for name in ("O365_CLIENT_ID", "O365_TENANT", "O365_SITE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("O365_HOME", str(home))


def test_the_environment_wins_over_the_file_and_the_page_names_the_file(tmp_path, monkeypatch, capsys) -> None:
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com", "client_id": "from-the-file"})
    _clean(monkeypatch, home)
    monkeypatch.setenv("O365_CLIENT_ID", "from-the-shell")

    assert cli._resolved("client_id", cli._prefs()) == ("from-the-shell", "environment")

    monkeypatch.delenv("O365_CLIENT_ID")
    assert cli.config([]) == 0
    out = capsys.readouterr().out
    assert "from-the-file" in out  # each value beside the file that answered it
    assert str(home / "config.json") in out
    assert f"file         {home / 'config.json'}" in out and "read only" in out


def test_the_advice_is_a_file_that_parses_and_keeps_what_is_already_answered(tmp_path, monkeypatch, capsys) -> None:
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com"})
    _clean(monkeypatch, home)

    advice = cli._advice(["client_id"])
    document = json.loads(textwrap.dedent(advice.split("<<'EOF'\n", 1)[1].split("EOF", 1)[0]))
    assert document == {"tenant": "contoso.onmicrosoft.com", "client_id": cli.EXAMPLES["client_id"]}
    assert str(home / "config.json") in advice

    # A login that cannot start prints that file rather than a path to guess.
    assert cli.main(["login"]) == REFUSED
    err = capsys.readouterr().err
    assert "no client id yet" in err
    assert f"cat > {home / 'config.json'} <<'EOF'" in err


def test_one_setting_answers_a_value_and_exits_one_when_nothing_does(tmp_path, monkeypatch, capsys) -> None:
    home = _home(tmp_path, {"tenant": "contoso.onmicrosoft.com"})
    _clean(monkeypatch, home)

    assert cli.config(["tenant"]) == 0
    assert capsys.readouterr().out.strip() == "contoso.onmicrosoft.com"

    assert cli.config(["client_id"]) == 1
    assert "no client id yet" in capsys.readouterr().err


# --- doctor ------------------------------------------------------------------------


def _jwt(**claims: Any) -> str:
    """A token whose payload carries ``claims``; the signature is never read."""
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return f"e30.{payload}.sig"


def _store(monkeypatch: pytest.MonkeyPatch, tmp_path: Any, **sessions: Any) -> None:
    """Put these sessions where ``O365_HOME`` points, so no test reads the real store."""
    monkeypatch.setenv("O365_HOME", str(tmp_path))
    (tmp_path / "sessions.json").write_text(json.dumps(sessions), "utf-8")


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


def test_a_page_with_no_markable_route_is_a_sentence_not_an_exit(monkeypatch, tmp_path, capsys) -> None:
    """No session still leaves the product block answerable, and exits 0."""
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_live_graph", lambda: pytest.fail("no session means no client"))

    assert cli.main(["doctor"]) == 0

    printed = capsys.readouterr().out
    assert printed.startswith("doctor: attention — no session; run o365 login")
    assert "PRODUCT" in printed and "intune" in printed


def test_a_route_marks_the_licence_its_type_declares_and_the_grant_its_token_carries(monkeypatch, tmp_path, capsys):
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_live_graph", lambda: None)
    monkeypatch.setattr(cli, "_held_plans", lambda client: frozenset({"INTUNE_A"}))
    assert cli.main(["doctor", "intune", "managed-device", "retire"]) == 0
    printed = capsys.readouterr().out
    assert "INTUNE_A" in printed and "have" in printed

    # A user's token answers the delegated flow and cannot answer the application one.
    _store(
        monkeypatch,
        tmp_path,
        graph={
            "mode": "device-flow",
            "constructor": {},
            "token": {"access_token": _jwt(aud=GRAPHS, scp="User.ReadWrite.All")},
        },
    )
    assert cli.main(["doctor", "directory", "user", "delete"]) == 0
    printed = capsys.readouterr().out
    assert "delegated" in printed and "have" in printed
    assert "application" in printed and "unknown" in printed
    assert "unknown is not missing" in printed


def test_what_the_model_does_not_describe_is_reported_and_a_typo_is_refused(monkeypatch, tmp_path, capsys) -> None:
    _store(monkeypatch, tmp_path)

    assert cli.main(["doctor", "intune", "managed-device", "list"]) == 0
    assert "declares no permission" in capsys.readouterr().out

    assert cli.main(["doctor", "intune", "managed-devicez"]) == REFUSED
    assert "did you mean managed-device" in capsys.readouterr().err


def test_the_page_lists_only_products_that_name_a_licence_and_wide_lists_all(monkeypatch, tmp_path, capsys) -> None:
    _store(monkeypatch, tmp_path)
    monkeypatch.setattr(cli, "_tenant_facts", _facts)

    assert cli.main(["doctor"]) == 0
    printed = capsys.readouterr().out
    assert "LICENSED" in printed and "booking" not in printed  # twenty rows of zeroes say it worse
    assert "no licence is named under the other" in printed
    assert "roles: 1 held — Global Administrator" in printed

    assert cli.main(["doctor", "-o", "wide"]) == 0
    printed = capsys.readouterr().out
    assert "\n  intune.devices" in printed  # the report behind the page
    assert "booking" in printed
    assert "no licence is named under" not in printed


def test_the_verdict_says_only_one_of_three_things() -> None:
    expired = {"sharepoint": {"mode": "device-flow", "claims": {"exp": int(time.time()) - 60}}}
    assert cli._verdict(expired, {"why": "", "roles": ("Global Administrator",)}, []) == (
        "doctor: attention — the sharepoint session expired; run o365 sharepoint login"
    )

    # ``unknown`` is not ``no``: a licence that could not be read is not one the tenant lacks.
    live = {"graph": {"mode": "device-flow", "claims": {"exp": int(time.time()) + 600}}}
    unread = {"why": "the tenant's subscriptions could not be read: is Licence.Read.All granted?", "roles": None}
    assert cli._verdict(live, unread, []) == (
        "doctor: unread — the tenant's subscriptions could not be read: is Licence.Read.All granted?"
    )

    records = [{"held": "yes"}, {"held": "no"}]
    assert cli._verdict(live, {"why": "", "roles": ("A", "B")}, records) == (
        "doctor: ok — 1 session, 1 of 2 licences, 2 roles"
    )


def test_a_product_page_counts_its_nouns_and_names_what_the_missing_ones_take(monkeypatch, tmp_path, capsys) -> None:
    """Six nouns waiting on one scope are one row: the name to grant, not the wall it unblocks."""
    _store(
        monkeypatch,
        tmp_path,
        graph={"mode": "device-flow", "constructor": {}, "token": {"access_token": _jwt(aud=GRAPHS, scp="User.Read")}},
    )
    monkeypatch.setattr(cli, "_live_graph", lambda: pytest.fail("outlook names no licence and no role"))

    assert cli.main(["doctor", "outlook"]) == 0
    printed = capsys.readouterr().out
    assert "37 nouns" in printed and "RESULT" in printed
    assert printed.count("Place.Read.All") == 1
    assert "PERMISSION" not in printed


def test_unmarked_is_not_have_and_an_unread_licence_is_not_missing() -> None:
    gates = cli.Gates(claims=None, held=frozenset(), assigned=frozenset(), roles=(), why="")
    assert cli._statement_row(cli.Statement("thing", (), TENANT, (), ()), gates)["result"] == cli.UNMARKED

    statement = cli.Statement("managed-device", ("INTUNE_A",), TENANT, (), ())
    unread = cli._statement_row(statement, cli.Gates(None, None, None, (), "could not be read"))
    absent = cli._statement_row(statement, cli.Gates(None, frozenset(), frozenset(), (), ""))
    assert unread["result"] == "unknown"
    assert absent["result"] == "missing" and absent["needs"] == "licence INTUNE_A"


# --- licences ----------------------------------------------------------------------


def _document(entries):
    """An index document with one product holding these ``(type ref, plans, seat)`` records."""
    return {
        "products": {
            "intune": {
                f"noun{position}": {
                    "noun": f"noun{position}",
                    "type": ref,
                    "licence": {"plans": list(plans), "seat": seat},
                }
                for position, (ref, plans, seat) in enumerate(entries)
            }
        }
    }


#: Two areas under one plan and seat, so grouping has something to do.
DOCUMENT = _document(
    [
        ("office365.intune.devices.managed.device:ManagedDevice", ("INTUNE_A",), TENANT),
        ("office365.intune.devices.managed.overview:ManagedDeviceOverview", ("INTUNE_A",), TENANT),
        ("office365.intune.policies.compliance:DeviceCompliancePolicy", ("INTUNE_A",), TENANT),
        ("office365.intune.devices.managed.seat:AssignedSeat", ("AAD_PREMIUM_P2",), USER),
    ]
)


def test_a_plan_is_one_licence_over_the_areas_that_declare_it() -> None:
    assert area_of("office365.intune.devices.management.managed.device:ManagedDevice") == "intune.devices"
    assert area_of("office365.directory.policies.conditional_access:Policy") == "directory.policies"

    found = [item for item in of(DOCUMENT) if item.plans == ("INTUNE_A",)][0]
    assert [family.name for family in found.families] == ["intune.devices", "intune.policies"]
    assert [family.nouns for family in found.families] == [2, 1]
    assert found.nouns == sum(family.nouns for family in found.families)  # no noun counted twice
    # The same plan is a different claim when the caller's own seat has to hold it,
    # and the plan that opens the most words leads.
    assert [item.seat for item in of(DOCUMENT)] == [TENANT, USER]
    assert [item.name for item in of(DOCUMENT)] == ["INTUNE_A", "AAD_PREMIUM_P2"]


def _answers(found):
    """The answer per seat, so a test asserts a fact rather than the order rows arrived in."""
    return {row["seat"]: row["held"] for row in found}


def test_a_seat_is_answered_from_the_read_that_owns_it() -> None:
    # A tenant seat is held by what the subscriptions provision; a user seat by the caller's own.
    assert _answers(rows(of(DOCUMENT), held=["INTUNE_A", "AAD_PREMIUM_P2"], mine=["TEAMS1"])) == {TENANT: YES, USER: NO}
    assert _answers(rows(of(DOCUMENT), held=["TEAMS1"], mine=["AAD_PREMIUM_P2"])) == {TENANT: NO, USER: YES}
    # A token without ``User.Read.All`` cannot answer, and must not accuse the tenant.
    assert _answers(rows(of(DOCUMENT), held=["INTUNE_A"], mine=None)) == {TENANT: YES, USER: UNKNOWN}
    assert [row["held"] for row in rows(of(DOCUMENT), held=["INTUNE_A"], mine=None)] == [YES, UNKNOWN]


def test_a_product_counts_its_words_and_those_that_name_a_licence() -> None:
    assert products(DOCUMENT) == [{"product": "intune", "nouns": 4, "licensed": 4}]
    # Zero licensed is a fact about the model, not about the tenant: no tenant is read.
    admin = {"products": {"admin": {"noun0": {"type": "office365.admin.exchange.client:Client"}}}}
    assert products(admin) == [{"product": "admin", "nouns": 1, "licensed": 0}]


def test_the_headline_is_a_verdict_not_a_count() -> None:
    assert headline(rows(of(DOCUMENT), held=["INTUNE_A"], mine=None), "contoso.onmicrosoft.com") == (
        "contoso.onmicrosoft.com: holds 1 of 2 licences a command names; 1 could not be read"
    )
    assert headline(rows(of(DOCUMENT), held=["INTUNE_A"], mine=[])) == (
        "holds 1 of 2 licences a command names; missing AAD_PREMIUM_P2"
    )
    both = rows(of(DOCUMENT), held=["INTUNE_A", "AAD_PREMIUM_P2"], mine=["AAD_PREMIUM_P2"])
    assert headline(both) == "holds all 2 licences a command names"


def test_the_licence_table_counts_areas_and_wide_prints_them_as_lines() -> None:
    """Eleven module names in a 48-column cell come out as `intune.…`; `2` says more."""
    counted = rows(of(DOCUMENT), frozenset({"INTUNE_A"}), frozenset())
    printed = cli._licence_table(counted, wide=False)
    assert "AREAS" in printed and "\u2026" not in printed
    assert [record["areas"] for record in counted] == [2, 1]

    lines = cli._licence_table(counted, wide=True).splitlines()
    assert lines[0].split()[0] == "INTUNE_A"  # the plan once, its areas as lines under it
    assert any(line.startswith("  intune.devices") for line in lines)
    assert printed.count("INTUNE_A") == 1 and "(2)" not in printed

    # Under *holds all 4*, HELD is a header over nothing.
    every = rows(of(DOCUMENT), frozenset({"INTUNE_A", "AAD_PREMIUM_P2"}), frozenset({"AAD_PREMIUM_P2"}))
    assert "HELD" not in cli._licence_table(every, wide=False)
