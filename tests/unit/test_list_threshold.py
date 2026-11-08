"""The list-view-threshold guard: what is warned about, and what is refused.

SharePoint blocks a query that filters or sorts on a non-indexed column once the
list passes the threshold, so the library has one guard in three places: a query
warns before the round trip rather than letting the server answer an opaque 500, a
single-shot load that fills the threshold says it may have been trimmed, and
``check_query`` refuses a call it already knows the service will reject. Each is
deliberately silent when it has nothing actionable to say.
"""

from __future__ import annotations

import warnings

import pytest
from office365.migration.offline import offline_sharepoint_context
from office365.runtime.client_object_collection import ClientObjectCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.exceptions import SPQueryThrottledException
from office365.sharepoint.fields.field import Field
from office365.sharepoint.listitems.caml import Caml, CamlQuery
from office365.sharepoint.listitems.caml.guard import threshold_warnings, warn_if_unpaged
from office365.sharepoint.lists.list import List
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD
from tests._scripted_transport import ScriptedTransport


def _query(column: str = "Status", *, paged: bool = False) -> CamlQuery:
    builder = CamlQuery.builder().where(Caml.text(column).eq("Active"))
    return (builder.row_limit(500) if paged else builder).build()


def _large() -> int:
    return LIST_VIEW_THRESHOLD * 2


def test_a_list_at_the_threshold_is_not_warned_about():
    assert threshold_warnings(_query(), item_count=LIST_VIEW_THRESHOLD) == []


def test_a_paged_query_is_never_warned_about():
    assert threshold_warnings(_query(paged=True), item_count=_large()) == []


def test_an_unpaged_query_over_a_large_list_names_the_column_to_index():
    (warning,) = threshold_warnings(_query(), item_count=_large())

    assert "'Status'" in warning, "the warning names the column the query filters on"
    assert "ensure_indexed('Status')" in warning, "and how to fix it"
    assert "page_size=" in warning, "or the paging argument that sidesteps it"


def test_an_unpaged_query_with_no_columns_and_unknown_size_is_silent():
    """``create_all_items_query`` reads everything anyway; there is nothing to index."""
    assert threshold_warnings(CamlQuery.create_all_items_query()) == []


def test_warn_if_unpaged_emits_one_user_warning():
    with pytest.warns(UserWarning, match="list view threshold"):
        warn_if_unpaged(_query(), item_count=_large())


def _list(item_count: int) -> List:
    lst = List(offline_sharepoint_context(), ResourcePath("lists/getByTitle('Tasks')"))
    lst.set_property("ItemCount", item_count)
    return lst


def test_get_items_only_warns_when_the_caller_did_not_ask_for_pages():
    lst = _list(_large())

    with pytest.warns(UserWarning, match="list view threshold"):
        lst.get_items(_query())
    lst.get_items(_query(), page_size=500)  # paged: the guard stays quiet


class _ThresholdCollection(ClientObjectCollection):
    _list_view_threshold = 3
    _truncation_hint = "page it"


def test_a_load_that_fills_the_threshold_warns_once_however_many_rows_arrive():
    collection = _ThresholdCollection(offline_sharepoint_context(), Field, ResourcePath("x"))

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for _ in range(_ThresholdCollection._list_view_threshold + 2):
            collection.add_child(Field(collection.context))

    (warning,) = [w for w in caught if issubclass(w.category, UserWarning)]
    assert "page it" in str(warning.message)


def test_check_query_raises_for_non_indexed_column():
    context = offline_sharepoint_context()
    context.pending_request().beforeExecute.clear()
    transport = ScriptedTransport(
        [
            {"d": {"ItemCount": 6000}},
            {"d": {"results": [{"InternalName": "date", "Title": "date", "Indexed": False}]}},
        ]
    )
    context.pending_request().transport = transport
    lst = context.web.lists.get_by_title("X")

    with pytest.raises(SPQueryThrottledException, match="date"):
        lst.check_query(CamlQuery.builder().order_by("date").build())
