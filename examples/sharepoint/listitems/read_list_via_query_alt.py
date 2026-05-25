"""Demonstrates how to read list items using render_list_data with a CAML query

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username


def print_progress(items_read: int):
    print("Items read: {0}".format(items_read))


def create_paged_query(page_size: int):
    qry = CamlQuery()
    qry.ViewXml = f"""
    <View Scope='RecursiveAll'>
       <Query></Query>
       <QueryOptions><QueryThrottleMode>Override</QueryThrottleMode></QueryOptions>
       <RowLimit Paged='TRUE'>{page_size}</RowLimit>
   </View>
   """
    return qry


ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = ctx.web.lists.get_by_title("Contacts_Large")
list_qry = create_paged_query(50)
assert list_qry.ViewXml is not None
result = target_list.render_list_data(list_qry.ViewXml).execute_query()
data = json.loads(result.value)
rows = data.get("Row", [])
print(len(rows))
