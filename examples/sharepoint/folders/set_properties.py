"""
Demonstrates how to update folder properties.

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

folder_url = "Shared Documents/Archive"
folder = ctx.web.get_folder_by_server_relative_path(folder_url)
folder_item = folder.list_item_all_fields
prop_name = "DocScope"
prop_value = "Public"
folder_item.set_property(prop_name, prop_value).update().execute_query()
