"""
Retrieves and prints the effective permission levels for a user on a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from pprint import pprint

from office365.sharepoint.client_context import ClientContext
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
pprint(result.value.permission_levels)  # print all permission levels
