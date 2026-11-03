"""The list-view-threshold guard: when an unpaged CAML query is warned about.

SharePoint blocks a query that filters or sorts on a non-indexed column once the
list passes the threshold, so ``get_items`` warns before the round trip rather
than letting the server answer an opaque 500. The guard is deliberately silent
when it has nothing actionable to say.
"""

from __future__ import annotations

import pytest
from office365.migration.offline import offline_sharepoint_context
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.listitems.caml import Caml, CamlQuery
from office365.sharepoint.listitems.caml.guard import threshold_warnings, warn_if_unpaged
from office365.sharepoint.lists.list import List
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD


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
    context = offline_sharepoint_context()
    lst = List(context, ResourcePath("lists/getByTitle('Tasks')"))
    lst.set_property("ItemCount", item_count)
    return lst


def test_get_items_only_warns_when_the_caller_did_not_ask_for_pages():
    lst = _list(_large())

    with pytest.warns(UserWarning, match="list view threshold"):
        lst.get_items(_query())
    lst.get_items(_query(), page_size=500)  # paged: the guard stays quiet
