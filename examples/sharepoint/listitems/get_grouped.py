"""Demonstrates how to retrieve grouped values from a list using render_list_data

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import json

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

view_xml = """
   <View>
       <Query>
          <GroupBy Collapse="TRUE" GroupLimit="100">
             <FieldRef Name="Author"/>
          </GroupBy>
       </Query>
       <ViewFields>
           <FieldRef Name="Author"/>
       </ViewFields>
       <RowLimit Paged="TRUE">100</RowLimit>
   </View>
   """

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
lib = ctx.web.lists.get_by_title("Site Pages")
result = lib.render_list_data(view_xml).execute_query()
data = json.loads(result.value)
for item in data.get("Row"):
    print(item.get("Author.title"))
