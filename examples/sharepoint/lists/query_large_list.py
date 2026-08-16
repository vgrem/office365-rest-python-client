"""Demonstrates how to query a large list with a CAML query filtered by a field

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def build_custom_query(page_size: int = 1000) -> CamlQuery:
    """Build a paged CAML query filtering list items by the 'WorkCountry' field."""
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Eq>
                 <FieldRef Name='WorkCountry'/>
                 <Value Type='Text'>United States</Value>
              </Eq>
           </Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
list_title = "Contacts_Large"
target_list = ctx.web.lists.get_by_title(list_title)

fields = target_list.fields.get().execute_query()

items = target_list.get_items(build_custom_query()).execute_query()
print(f"Total items count: {len(items)}")
for index, item in enumerate(items):
    title = item.properties.get("Title")
    country = item.properties.get("WorkCountry")
    print(f"{index}: {title} ({country})")
