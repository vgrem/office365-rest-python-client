"""
Demonstrates how to create a new folder.

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


folder_name = "Reports"  # creates a temporary folder first in Documents library
folder = (
    ctx.web.default_document_library().root_folder.folders.add_using_path(folder_name, overwrite=True).execute_query()
)
print("Folder : {0} has been created".format(folder.server_relative_url))
