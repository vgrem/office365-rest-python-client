"""Which object a request is built on: the feed for a list, the item for every other verb.

This pins a defect rather than a shape. A ``list`` is ``get()`` on the feed, but the walk was
taken to the *item* type, which is a different object two ways: ``Message`` is not reachable
from the root at all, so listing messages was refused as unwalkable, and ``User`` is reachable —
through ``me`` — so ``o365 directory user list`` sent ``GET /me`` and printed the caller as if
it were the user list.
"""

from office365.cli import _walk
from office365.graph_client import GraphClient
from office365.routing import route


def test_a_list_walks_to_the_feed_and_not_to_one_item_of_it():
    assert _walk(GraphClient, route("outlook", "message", "list")) == ("me", "messages")
    assert _walk(GraphClient, route("directory", "user", "list")) == ("users",)


def test_a_list_follows_every_root_link_the_route_names():
    assert _walk(GraphClient, route("intune", "managed-device", "list")) == ("device_management", "managed_devices")


def test_a_feed_reachable_only_through_one_item_is_refused():
    """``attachments`` hangs off one ``Message``, and no link names the id to address it by."""
    assert _walk(GraphClient, route("outlook", "message", "attachments", "list")) is None


def test_a_single_item_is_still_the_target_of_a_get():
    assert _walk(GraphClient, route("onedrive", "drive", "get")) == ("me", "drive")
