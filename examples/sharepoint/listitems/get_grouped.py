"""Demonstrates how to retrieve grouped values from a list using render_list_data

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import json

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

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

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.lists.get_by_title("Site Pages")
result = lib.render_list_data(view_xml).execute_query()
data = json.loads(result.value)
for item in data.get("Row"):
    print(item.get("Author.title"))
