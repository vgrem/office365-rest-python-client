"""
Demonstrates how to upload a JSON file to a SharePoint site
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

list_title = "Documents"
folder = ctx.web.lists.get_by_title(list_title).root_folder
path = "../../data/countries.json"
with open(path, "r") as f:
    file = folder.files.upload(f).execute_query()
print(f"File has been uploaded into: {file.server_relative_url}")
