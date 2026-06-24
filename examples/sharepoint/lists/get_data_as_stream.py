"""Demonstrates how to retrieve SharePoint list data as a stream using a CAML query

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url
from tests.settings import tenant, username, client_id, password

ctx = ClientContext(test_team_site_url).with_username_and_password(tenant, client_id, username, password)

view_xml = """
<View>
    <Query>
        <Where>
        </Where>
    </Query>
     <ViewFields>
        <FieldRef Name='Title' />
        <FieldRef Name='Created' />
        <FieldRef Name='Author' />
    </ViewFields>
    <RowLimit>100</RowLimit>
</View>
"""


result = ctx.web.get_list_data_as_stream("/Shared Documents", view_xml=view_xml).execute_query()
print(result.value)
