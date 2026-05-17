"""
Demonstrates how to retrieve folders.
If the 'recursive' flag is set to True, it traverses all sub folders.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
folders = ctx.web.default_document_library().root_folder.get_folders(False).execute_query()
for folder in folders:
    print(f"Url: {folder.server_relative_url}, Created: {folder.time_created}")
