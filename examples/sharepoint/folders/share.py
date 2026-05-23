"""
Demonstrates how to share a folder with a user.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.external_site_option import ExternalSharingSiteOption
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_user_principal_name, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
folder_url = "Shared Documents/Archive"
folder = ctx.web.get_folder_by_server_relative_path(folder_url)
result = folder.list_item_all_fields.share(test_user_principal_name, ExternalSharingSiteOption.View).execute_query()
print(result.url)
