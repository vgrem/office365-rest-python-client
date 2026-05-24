"""
Demonstrates how to assign custom permissions on a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.role_type import RoleType
from tests import (
    test_client_id,
    test_client_secret,
    test_site_url,
    test_tenant,
    test_user_principal_name,
)

client = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/Financial Sample.xlsx"


role_def = client.web.role_definitions.get_by_type(RoleType.Contributor)
user = client.web.site_users.get_by_principal_name(test_user_principal_name)
target_file = client.web.get_file_by_server_relative_path(file_url)

# assign a custom permissions for the user to a file
target_file.listItemAllFields.add_role_assignment(user, role_def).execute_query()
