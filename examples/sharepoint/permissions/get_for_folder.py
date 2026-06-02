"""
Get effective permissions for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
folder_url = "Shared Documents/Reports"
folder = ctx.web.get_folder_by_server_relative_url(folder_url)
result = folder.get_user_effective_permissions(ctx.web.current_user).execute_query()
for level in result.value.permission_levels:
    print(level)
