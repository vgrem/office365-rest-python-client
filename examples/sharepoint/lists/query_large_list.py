"""Query a large list with a paged CAML query filtered by a field.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def build_custom_query(field: str, value: str, page_size: int = 5000) -> CamlQuery:
    """Build a paged CAML query filtering list items by a text field."""
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Neq>
                 <FieldRef Name='{field}'/>
                 <Value Type='Text'>{value}</Value>
              </Neq>
           </Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


def main():
    p = argparse.ArgumentParser(description="Query a large SharePoint list with a CAML query")
    p.add_argument("--list-title", default="Stocks_5yr_Large", help="list title")
    # "Name" collides with the built-in FileLeafRef field, so the importer stores
    # that column as "Name_" (see List.from_dataframe).
    p.add_argument("--field", default="Name_", help="field to filter on")
    p.add_argument("--value", default="AAPL", help="value to match")
    p.add_argument("--page-size", type=int, default=5000, help="items per page")
    args = p.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    items = target_list.get_items(build_custom_query(args.field, args.value, args.page_size)).execute_query()
    print(f"Total items count: {len(items)}")
    for index, item in enumerate(items):
        name = item.properties.get(args.field)
        date = item.properties.get("date")
        close = item.properties.get("close")
        print(f"{index}: {name} {date} close={close}")


if __name__ == "__main__":
    main()
