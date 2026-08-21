"""
Read all items from a large list using a CAML query filtered by a field.

Filters ``Contacts_Large`` by ``WorkCountry == 'England'`` and reads every
matching row with server-driven paging (page size = RowLimit).

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.listitems.collection import ListItemCollection
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

FIELD_NAME = "WorkCountry"
FIELD_VALUE = "France"


def build_custom_query(page_size: int = 1000) -> CamlQuery:
    """Build a paged CAML query filtering list items by WorkCountry."""
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Neq>
                 <FieldRef Name='{FIELD_NAME}'/>
                 <Value Type='Text'>{FIELD_VALUE}</Value>
              </Neq>
           </Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


def print_progress(items: ListItemCollection) -> None:
    print(f"  items read so far: {len(items)}")


def main():
    parser = argparse.ArgumentParser(description="Read a large list with a CAML query filter")
    parser.add_argument("--list-title", default="Contacts_Large", help="Target list title")
    parser.add_argument("--page-size", type=int, default=2000, help="Items per page (RowLimit)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title(args.list_title)

    items = target_list.get_items(build_custom_query(args.page_size))
    items.paged(args.page_size, page_loaded=print_progress)
    items.execute_query()

    count = 0
    for item in items:
        count += 1
        title = item.properties.get("Title", "?")
        country = item.properties.get(FIELD_NAME, "?")
        print(f"  {item.id}: {title} ({country})")

    print(f"Total items with {FIELD_NAME} == '{FIELD_VALUE}': {count}")


if __name__ == "__main__":
    main()
