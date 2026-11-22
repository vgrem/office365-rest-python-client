"""Which object a request is built on: the feed for a list, the item for every other verb.

This pins a defect rather than a shape. A ``list`` is ``get()`` on the feed, but the walk was
taken to the *item* type, which is a different object two ways: ``Message`` is not reachable
from the root at all, so listing messages was refused as unwalkable, and ``User`` is reachable —
through ``me`` — so ``o365 directory user list`` sent ``GET /me`` and printed the caller as if
it were the user list.

The other half is the key that names *one* item: ``--id`` indexes the feed the walk reached, so
``user delete --id <upn>`` is ``DELETE /users/<upn>`` and not ``DELETE /me``, and a route no key
can complete is refused without promising a flag the command does not declare.
"""

from office365 import cli
from office365.cli import _feed, _keyed, _walk
from office365.graph_client import GraphClient
from office365.routing import route

#: What `_refuse` answers with when it refused before sending anything.
REFUSED = 2


def test_a_list_walks_to_the_feed_and_not_to_one_item_of_it():
    assert _walk(GraphClient, route("outlook", "message", "list")) == ("me", "messages")
    assert _walk(GraphClient, route("directory", "user", "list")) == ("users",)


def test_a_list_follows_every_root_link_the_route_names():
    assert _walk(GraphClient, route("intune", "managed-device", "list")) == ("device_management", "managed_devices")


def test_a_feed_reachable_only_through_one_item_is_refused():
    """``attachments`` hangs off one ``Message``: without ``--id`` no link names the key."""
    assert _walk(GraphClient, route("outlook", "message", "attachments", "list")) is None


def test_a_single_item_is_still_the_target_of_a_get():
    assert _walk(GraphClient, route("onedrive", "drive", "get")) == ("me", "drive")


def test_a_key_names_the_item_the_verb_acts_on():
    """``user delete --id <upn>`` deletes that user: the feed the noun states, indexed by the key."""
    found = route("directory", "user", "delete")
    assert _keyed(found, getattr(found.here, found.method))
    assert _feed(GraphClient, found, "directory") == ("users",)


def test_a_feed_reached_through_one_item_takes_that_items_key():
    """``message attachments list --id <id>`` addresses a message, then reads its attachments."""
    found = route("outlook", "message", "attachments", "list")
    assert _feed(GraphClient, found, "outlook") == ("me", "messages")


def test_a_create_has_no_item_for_a_key_to_name():
    found = route("directory", "user", "create")
    assert _keyed(found, getattr(found.here, found.method)) is False


def test_a_key_is_what_the_dry_run_prints(monkeypatch, capsys):
    """Nothing is sent, so the client needs no token: the URL is asked of the model."""
    monkeypatch.setattr(cli, "_client", lambda *word, **rest: GraphClient())
    assert cli.command("directory", ["user", "delete"], ["--id", "a.dyukov@contoso.com", "-n", "--yes"]) == 0
    printed = capsys.readouterr().out
    assert printed.strip() == "DELETE https://graph.microsoft.com/v1.0/users/a.dyukov@contoso.com"


def test_a_route_a_key_would_complete_says_so(monkeypatch, capsys):
    monkeypatch.setattr(cli, "_client", lambda *word, **rest: GraphClient())
    assert cli.command("outlook", ["message", "attachments", "list"], []) == REFUSED
    assert capsys.readouterr().err.rstrip().endswith("; --id names it")


def test_a_noun_with_no_feed_is_not_offered_a_key(monkeypatch, capsys):
    """The refusal must not promise a flag the command does not declare."""
    monkeypatch.setattr(cli, "_client", lambda *word, **rest: GraphClient())
    assert cli.command("directory", ["administrative-unit", "get"], []) == REFUSED
    assert "--id" not in capsys.readouterr().err
