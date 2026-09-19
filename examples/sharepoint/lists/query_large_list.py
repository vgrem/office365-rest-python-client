"""Query a large list with a CAML query (reproduces the list view threshold error).

The query filters on a **non-indexed** column (``Name_``) and matches almost every
item. On a list larger than the 5,000-item list view threshold SharePoint rejects
it with HTTP 500 / ``SPException -2147467259 "Cannot complete this action. Please
try again."`` — the error reported in issue #427.

To fix it, filter on an indexed column (``ID`` is always indexed, e.g. ``ID > 0``)
or add an index to the column you filter on (List settings -> Indexed columns).

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def build_custom_query(page_size: int = 10000) -> CamlQuery:
    """Build a CAML query filtered on a non-indexed column (breaks the threshold).

    Note there is **no** ``Paged='TRUE'`` here: with paging SharePoint caps the
    page at the 5,000-item threshold and returns it without erroring. Without
    paging (and a ``RowLimit`` above the threshold) the request is rejected.
    """
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Neq>
                 <FieldRef Name='Name_'/>
                 <Value Type='Text'>__none__</Value>
              </Neq>
           </Where>
       </Query>
       <RowLimit>{page_size}</RowLimit>
    </View>
    """
    return qry


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
