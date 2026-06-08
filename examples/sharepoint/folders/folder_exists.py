"""
How to determine whether a folder exists.

Uses the ``Exists`` property. An alternative approach is to try
the request and handle FileNotFoundException (HTTP 404).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
folder_path = "Shared Documents"
folder = ctx.web.get_folder_by_server_relative_url(folder_path).select(["Exists"]).get().execute_query()
if folder.exists:
    print(f"Folder '{folder_path}' is found")
else:
    print(f"Folder '{folder_path}' not found")
