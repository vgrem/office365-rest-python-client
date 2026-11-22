"""What a command prints: one row per item, and no row for a feed that holds none.

This pins a defect seen on the first live read of an empty feed: `_rows` fell back to the feed
itself, so `o365 intune managed-device list` in a tenant with no devices printed the envelope —
`value  []` under a `VALUE` heading — instead of the sentence `_send` had built for that case.
"""

from office365.cli import _rows
from office365.directory.users.user import User
from office365.migration.offline import offline_context
from office365.runtime.client_object_collection import ClientObjectCollection


def _feed(*names: str) -> ClientObjectCollection:
    feed = ClientObjectCollection(offline_context(), User, None)
    for name in names:
        item = User(offline_context())
        item.set_property("displayName", name)
        feed.add_child(item)
    return feed


def test_a_feed_is_one_row_per_item() -> None:
    assert [row.display_name for row in _rows(_feed("a", "b"))] == ["a", "b"]


def test_an_empty_feed_is_no_rows_so_the_caller_prints_its_sentence() -> None:
    assert _rows(_feed()) == []
