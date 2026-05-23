"""
Demonstrates how to upload a CSV file to a SharePoint site
"""

import os

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

list_title = "Documents"
folder = ctx.web.lists.get_by_title(list_title).root_folder
path = "../../data/Financial Sample.csv"
with open(path, "r") as content_file:
    file_content = content_file.read().encode("utf-8-sig")
file = folder.upload_file(os.path.basename(path), file_content).execute_query()
print("File has been uploaded into: {0}".format(file.server_relative_url))
