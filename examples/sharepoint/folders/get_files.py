"""
Gets files within a folder.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_team_site_url

ctx = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)
root_folder = ctx.web.default_document_library().root_folder
ctx.load(root_folder, ["Files"])
ctx.execute_query()
for file in root_folder.files:
    print(file.name)
