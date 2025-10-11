"""
Demonstrates how to create a folder with a color
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.colors import FolderColors
from tests import test_client_id, test_client_secret, test_team_site_url

ctx = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)


root_folder = ctx.web.default_document_library().root_folder
folder = root_folder.folders.add("Report1234", color_hex=FolderColors.DarkGreen).execute_query()
print(f"Folder : {folder.server_relative_url} has been created")
