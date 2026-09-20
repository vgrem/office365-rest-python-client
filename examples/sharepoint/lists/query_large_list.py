"""Query a large list that returns more than the 5,000-item list view threshold.

Sorts by ``ID`` (always indexed, so the sort never trips the threshold) and pages
through every item with a typed CAML query built by the fluent builder. Pass
``--since`` to add a date filter; filtering on a non-indexed column needs an index,
which ``ensure_indexed`` enables (SharePoint then builds it in the background).

    python query_large_list.py --list-title Stocks_5yr_Large
    python query_large_list.py --list-title Stocks_5yr_Large --since 2013-01-01

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml import Caml, CamlQuery
from office365.sharepoint.views.scope import ViewScope
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

PREVIEW_ROWS = 5


def build_query(since: str | None, page_size: int) -> CamlQuery:
    """A typed, paged CAML query sorted by ``ID`` (optionally filtered by ``since``)."""
    builder = CamlQuery.builder().order_by("ID").row_limit(page_size, paged=True).scope(ViewScope.RecursiveAll)
    if since:
        builder.where(Caml.text("date").geq(since))
    return builder.build()


def main():
    parser = argparse.ArgumentParser(description="Query a large SharePoint list")
    parser.add_argument("--list-title", default="Stocks_5yr_Large", help="list title")
    parser.add_argument("--since", default=None, help="only rows on/after this date (default: all)")
    parser.add_argument("--page-size", type=int, default=2000, help="items per page (keep <= 5000)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    target_list.ensure_property("ItemCount").execute_query()
    print(f"List '{args.list_title}' has {target_list.item_count:,} item(s)")

    if args.since:
        # Index the filtered column so the filter is not throttled (idempotent).
        target_list.ensure_indexed("date").execute_query()

    # Page through every match (iterating continues from the last item's position).
    items = target_list.get_items(build_query(args.since, args.page_size), page_size=args.page_size).execute_query()
    scope = f" since {args.since}" if args.since else ""
    count = sum(1 for _ in items)
    print(f"Read {count} item(s){scope}")
    for index, item in enumerate(items):
        if index >= PREVIEW_ROWS:
            break
        print(f"{index}: {item.properties.get('Name_')} {item.properties.get('date')}")


if __name__ == "__main__":
    main()
