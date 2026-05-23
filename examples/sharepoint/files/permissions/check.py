"""
Demonstrates how to determine whether a user has permissions for a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.kind import PermissionKind
from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_user_principal_name_alt,
    test_username,
)

client = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
file_url = "Shared Documents/Financial Sample.xlsx"

target_user = client.web.site_users.get_by_email(test_user_principal_name_alt)
target_file = client.web.get_file_by_server_relative_path(file_url)
result = target_file.get_user_effective_permissions(target_user).execute_query()
# verify whether user has Reader role to a file
if result.value.has(PermissionKind.OpenItems):
    print("User has access to read a file")
