"""
Demonstrates how to upload a large file using chunked upload session.

See https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest#working-with-large-files-by-using-rest
"""

import os

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username


def print_upload_progress(offset: int) -> None:
    file_size = os.path.getsize(local_path)
    print(f"Uploaded '{offset}' bytes from '{file_size}'...[{round(offset / file_size * 100, 2)}%]")


ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

target_url = "Shared Documents/archive"
target_folder = ctx.web.get_folder_by_server_relative_url(target_url)
size_chunk = 1000000
local_path = "../../../tests/data/big_buck_bunny.mp4"
with open(local_path, "rb") as f:
    uploaded_file = target_folder.files.create_upload_session(f, size_chunk, print_upload_progress).execute_query()

print(f"File {uploaded_file.server_relative_url} has been uploaded successfully")
