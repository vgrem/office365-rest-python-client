"""Demonstrates how to upload a JSON file to a SharePoint site"""

from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_user_credentials

ctx = ClientContext(test_team_site_url).with_credentials(test_user_credentials)

list_title = "Documents"
folder = ctx.web.lists.get_by_title(list_title).root_folder
path = "../../data/countries.json"
with open(path) as f:
    file = folder.files.upload(f).execute_query()
print(f"File has been uploaded into: {file.serverRelativeUrl}")
