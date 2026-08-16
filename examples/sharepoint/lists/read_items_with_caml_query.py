"""Demonstrates how to retrieve list items using a CAML query

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import datetime

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)


def build_custom_query(page_size: int = 100) -> CamlQuery:
    """ "
    :type page_size: int
    """
    from_datetime = datetime.datetime(2022, 1, 20, 0, 0)
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query>
           <Where>
              <Gt>
                 <FieldRef Name='Created'/>
                 <Value Type='DateTime' IncludeTimeValue='True'>{from_datetime.isoformat()}</Value>
              </Gt>
           </Where>
       </Query>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
    </View>
    """
    return qry


list_title = "Site Pages"
site_pages = ctx.web.lists.get_by_title(list_title)
items = site_pages.get_items(build_custom_query(5)).execute_query()
print(f"Total items count: {len(items)}")
for index, item in enumerate(items):
    print(f"{index}: {item.properties['Created']}")
