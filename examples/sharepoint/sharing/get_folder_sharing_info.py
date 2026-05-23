"""
Gets the sharing information for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

folder_url = "Shared Documents/Archive"
result = ctx.web.get_folder_by_server_relative_url(folder_url).get_sharing_information().execute_query()

for sharing_link in result.sharing_links:
    print(sharing_link)
