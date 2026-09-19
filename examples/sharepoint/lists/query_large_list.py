"""Query a large list with a CAML query.

The **default** query filters on the always-indexed ``ID`` column (``ID > 0``):
it matches every item and — because ``ID`` is indexed — is not blocked by the
5,000-item list view threshold. ``RowLimit Paged='TRUE'`` plus server-driven
paging (``__next``) reads the whole list page by page.

Pass ``--reproduce`` to do the opposite: filter on a **non-indexed** column that
matches almost every item. On a list larger than the 5,000-item list view
threshold SharePoint rejects the request with HTTP 500 /
``SPException -2147467259 "Cannot complete this action. Please try again."`` —
the error reported in issue #427. Use it to confirm the threshold, then fix it by
filtering on an indexed column (like ``ID``) or by indexing the column you filter
on (List settings → Indexed columns).

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ID_FIELD = "ID"  # the built-in, always-indexed identifier column
UNINDEXED_FIELD = "Name_"  # a custom (non-indexed by default) column
PREVIEW_ROWS = 5  # how many rows to print as a preview


def build_query(field: str | None = None, value: str | None = None, page_size: int = 5000) -> CamlQuery:
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


def build_threshold_query(field: str, page_size: int) -> CamlQuery:
    """Build a query that breaks the list view threshold (#427).

    Filters on a **non-indexed** column with a condition that matches almost every
    item, so on a list larger than 5,000 items SharePoint rejects it.
    """
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Neq><FieldRef Name='{field}'/><Value Type='Text'>__none__</Value></Neq>
           </Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


def reproduce_threshold_error(target_list, field: str, page_size: int) -> None:
    """Run a single non-indexed GetItems request to trigger the #427 error."""
    print(f"Filtering on non-indexed column '{field}' (RowLimit={page_size}) ...")
    try:
        items = target_list.get_items(build_threshold_query(field, page_size)).execute_query()
    except ClientRequestException as ex:
        status = getattr(ex.response, "status_code", None)
        print("Reproduced #427 (list view threshold):")
        print(f"  HTTP status: {status}")
        print(f"  code:        {ex.code}")
        print(f"  message:     {ex.message}")
        print(
            "\nFix: filter on an indexed column (e.g. ID > 0) or add an index to "
            "the column you filter on (List settings -> Indexed columns)."
        )
    else:
        print(f"No error: read {len(items)} item(s).")
        print("The list is probably under the 5,000-item threshold, or the column is indexed.")


def main():
    parser = argparse.ArgumentParser(description="Query a large SharePoint list with a CAML query")
    parser.add_argument("--list-title", default="Stocks_5yr_Large", help="list title")
    parser.add_argument("--page-size", type=int, default=10000, help="items per page (RowLimit)")
    parser.add_argument("--limit", type=int, default=0, help="stop after N items (0 = all)")
    parser.add_argument("--field", help="optional field to filter on (e.g. Name_)")
    parser.add_argument("--value", help="optional value to match")
    parser.add_argument(
        "--reproduce",
        action="store_true",
        help="trigger the list view threshold error (#427): filter on a non-indexed column",
    )
    parser.add_argument(
        "--unindexed-field",
        default=UNINDEXED_FIELD,
        help="non-indexed column used by --reproduce",
    )
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    if args.reproduce:
        reproduce_threshold_error(target_list, args.unindexed_field, args.page_size)
        return

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
