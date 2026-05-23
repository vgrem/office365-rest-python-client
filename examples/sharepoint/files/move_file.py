"""
Demonstrates how to move a file within a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.move_operations import MoveOperations
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)


file_from = ctx.web.get_file_by_server_relative_path("Shared Documents/Financial Sample.xlsx")

# folder_to = ctx.web.get_folder_by_server_relative_url("Shared Documents")
folder_to = "Shared Documents/Archive"

file_to = file_from.move_to_using_path(folder_to, MoveOperations.overwrite).execute_query()
print(f"'{file_from}' moved into '{file_to.server_relative_path}'")
