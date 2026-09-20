"""CAML guards for the SharePoint **list view threshold**.

CAML parsing lives on :class:`~office365.sharepoint.listitems.caml.query.CamlQuery`
(``is_paged``/``field_refs``); this module owns the policy that turns it into
warnings and the columns worth indexing. It is a plain function API (not a
decorator), so it stays explicit and easy to test in isolation.
"""

from __future__ import annotations

import warnings
from typing import Optional

from office365.sharepoint.listitems.caml.query import CamlQuery

LIST_VIEW_THRESHOLD = 5000  # SharePoint's default list view threshold
_ALWAYS_INDEXED = frozenset({"ID"})  # ID is indexed by SharePoint


def indexing_candidates(query: CamlQuery) -> set[str]:
    """Field names referenced by the query that are worth indexing (``ID`` excluded)."""
    return {name for name in query.field_refs if name not in _ALWAYS_INDEXED}


def threshold_warnings(
    query: CamlQuery,
    *,
    item_count: Optional[int] = None,
    threshold: int = LIST_VIEW_THRESHOLD,
) -> list[str]:
    """Warnings for a CAML query that may exceed the list view threshold.

    Empty when the query is paged, when the list is known to be at/below the
    threshold, or when an unpaged query references no columns (a plain
    ``create_all_items_query`` on a list whose size is unknown).
    """
    if query.is_paged:
        return []
    if item_count is not None and item_count <= threshold:
        return []
    names = sorted(indexing_candidates(query))
    if not names and item_count is None:
        return []
    fields = f" on column(s) {', '.join(repr(name) for name in names)}" if names else ""
    hint = (
        f"index them with ensure_indexed(...) (e.g. lst.ensure_indexed({names[0]!r}).execute_query())"
        if names
        else "index the filtered/sorted columns with ensure_indexed(...)"
    )
    return [
        f"This CAML query is not paged and may exceed the SharePoint list view threshold "
        f"({threshold:,} items){fields}. Pass page_size=2000 to get_items(), add "
        f"RowLimit Paged='TRUE' and iterate, or {hint} to avoid throttling."
    ]


def warn_if_unpaged(
    query: CamlQuery,
    *,
    item_count: Optional[int] = None,
    threshold: int = LIST_VIEW_THRESHOLD,
) -> None:
    """Emit a :class:`UserWarning` per issue from :func:`threshold_warnings`."""
    for message in threshold_warnings(query, item_count=item_count, threshold=threshold):
        warnings.warn(message, stacklevel=3)
