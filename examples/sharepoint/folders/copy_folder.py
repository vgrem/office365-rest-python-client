"""
Demonstrates how to copy a folder within a site.

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

# creates a temporary folder first in a Documents library
# folder_from = ctx.web.default_document_library().root_folder.add(
#    create_unique_name("from")
# )
folder_from = ctx.web.get_folder_by_server_relative_url("Shared Documents/Archive/2001")

# folder_to = ctx.web.default_document_library().root_folder.add(create_unique_name("to"))
# folder_to_url = "/sites/team/Shared Documents/Archive/2001/01"
folder_to = ctx.web.get_folder_by_server_relative_url("Shared Documents/Archive/2002")

# copies the folder with a new name
folder = folder_from.copy_to(folder_to).execute_query()
print("Folder has been copied from '{0}' into '{1}'".format(folder_from.server_relative_url, folder.server_relative_url))

# clean up
# folder_from.delete_object().execute_query()
# folder.delete_object().execute_query()
