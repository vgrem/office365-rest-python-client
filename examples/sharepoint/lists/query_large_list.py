"""Query a large list with a typed CAML query (reproduces the list view threshold error).

The query is built with the fluent :class:`~office365.sharepoint.listitems.caml.builder.QueryBuilder`
instead of a raw ``ViewXml`` string. It filters on a **non-indexed** column
(``Name_``) and sorts on another (``date``); on a list larger than the 5,000-item
list view threshold SharePoint rejects it with HTTP 500 /
``SPException -2147467259 "Cannot complete this action. Please try again."`` —
the error reported in issue #427.

To fix it, filter/sort on an indexed column (``ID`` is always indexed, e.g.
``ID > 0``) or add an index to the column you filter on:

    target_list.ensure_indexed("date").execute_query()

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml import Caml, CamlQuery
from office365.sharepoint.views.scope import ViewScope
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def build_custom_query(page_size: int = 10000) -> CamlQuery:
    """Build a CAML query that breaks the list view threshold (#427).

    SharePoint Online silently **trims** a non-indexed ``<Where>`` to the 5,000
    item threshold, so a plain filter just returns 5,000 rows. Sorting on a
    **non-indexed** column (``OrderBy``) forces a full sort that cannot be
    trimmed, which is what makes SharePoint reject the request (HTTP 500 /
    ``SPException -2147467259 "Cannot complete this action. Please try again."``).
    """
    return (
        CamlQuery.builder()
        .where(Caml.text("Name_").neq("__none__"))
        .order_by("date")
        .row_limit(page_size, paged=False)
        .scope(ViewScope.RecursiveAll)
        .build()
    )


def main():
    parser = argparse.ArgumentParser(description="Query a large SharePoint list with a CAML query")
    parser.add_argument("--list-title", default="Stocks_5yr_Large", help="list title")
    parser.add_argument("--page-size", type=int, default=10000, help="items per page (RowLimit)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    items = target_list.get_items(build_custom_query(args.page_size)).execute_query()
    print(f"Total items count: {len(items)}")
    for index, item in enumerate(items):
        print(f"{index}: {item.properties.get('Name_')} {item.properties.get('date')}")


if __name__ == "__main__":
    main()
