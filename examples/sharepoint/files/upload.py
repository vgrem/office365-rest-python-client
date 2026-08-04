"""
Demonstrates how to upload small files (up to 4MB in size).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)

list_title = "Documents"
folder = ctx.web.lists.get_by_title(list_title).root_folder
path = "../../data/Financial Sample.xlsx"
with open(path, "rb") as f:
    file = folder.files.upload(f).execute_query()
print(f"File has been uploaded into: {file.server_relative_url}")
