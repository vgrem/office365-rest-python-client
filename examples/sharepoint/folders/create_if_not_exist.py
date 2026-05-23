"""
Returns a folder from a given site-relative path, creating it if it does not exist.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
folder_url = "Shared Documents/Archive/2023/10/1"
folder = ctx.web.ensure_folder_path(folder_url).get().select(["ServerRelativePath"]).execute_query()
print(folder.server_relative_path)
