"""Demonstrates how to use QueryThrottleMode override to bypass the list view threshold

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.caml.query import CamlQuery
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username


def create_paged_query(page_size):
    qry = CamlQuery()
    qry.ViewXml = f"""
       <View Scope='RecursiveAll'>
          <Query><Where><Neq>
          <FieldRef Name=\"FullName\" /><Value Type=\"Text\">Travis Clayton</Value>
          </Neq></Where></Query>
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
large_list = ctx.web.lists.get_by_title("Contacts_Large")
items = large_list.get_items(create_paged_query(100)).execute_query()
print(items)
