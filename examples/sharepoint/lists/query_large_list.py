"""Query a large list and read almost all of its items with a paged CAML query.

The broadest query filters on the always-indexed ``ID`` column (``ID > 0``): it
matches every item and — because ``ID`` is indexed — is not blocked by the
5,000-item list view threshold. ``RowLimit Paged='TRUE'`` plus server-driven
paging (``__next``) reads the whole list page by page, without loading it all at
once.

Pass ``--field``/``--value`` for a narrower filter, or ``--limit`` to stop early.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ID_FIELD = "ID"  # the built-in, always-indexed identifier column
PREVIEW_ROWS = 5  # how many rows to print as a preview


def build_query(field: str | None = None, value: str | None = None, page_size: int = 2000) -> CamlQuery:
    """Build a paged CAML query.

    With no ``field``/``value`` it filters on ``ID > 0`` — the broadest query that
    matches every item and, since ``ID`` is indexed, lets SharePoint page past the
    5,000-item list view threshold.
    """
    if field and value:
        where = f"<Gt><FieldRef Name='{field}'/><Value Type='Text'>{value}</Value></Gt>"
    else:
        where = f"<Gt><FieldRef Name='{ID_FIELD}'/><Value Type='Counter'>0</Value></Gt>"
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>{where}</Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


def main():
    parser = argparse.ArgumentParser(description="Query a large SharePoint list with a broad CAML query")
    parser.add_argument("--list-title", default="Stocks_5yr_Large", help="list title")
    parser.add_argument("--page-size", type=int, default=2000, help="items per page (RowLimit)")
    parser.add_argument("--limit", type=int, default=0, help="stop after N items (0 = all)")
    parser.add_argument("--field", help="optional field to filter on (e.g. Name_)")
    parser.add_argument("--value", help="optional value to match")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    # RowLimit Paged='TRUE' + paged(...): iterating follows __next page by page.
    items = target_list.get_items(build_query(args.field, args.value, args.page_size)).paged(args.page_size)
    target_list.context.execute_query()

    read = 0
    for item in items:
        read += 1
        if read <= PREVIEW_ROWS:
            name = item.properties.get("Name_") or item.properties.get("Title")
            print(f"{read}: id={item.id} Name={name} date={item.properties.get('date')}")
        if args.limit and read >= args.limit:
            break
    print(f"Read {read} item(s) from '{args.list_title}'")


if __name__ == "__main__":
    main()
