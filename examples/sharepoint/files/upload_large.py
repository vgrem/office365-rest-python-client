"""
Demonstrates how to upload a large file using chunked upload session.

See https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest#working-with-large-files-by-using-rest
"""

import os
from pathlib import Path
from typing import Any

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username


def print_progress(offset: int, *args: Any) -> None:
    file_size = os.path.getsize(local_path)
    pct = offset / file_size * 100
    print(f"Uploaded {offset} bytes / {file_size} bytes ({pct:.1f}%)")


local_path = Path("../../../tests/data/big_buck_bunny.mp4")
chunk_size_bytes = 1_000_000  # 1 MB

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

target_url = "Shared Documents/archive"
target_folder = ctx.web.get_folder_by_server_relative_url(target_url)

with open(str(local_path), "rb") as f:
    uploaded = target_folder.files.create_upload_session(f, chunk_size_bytes, print_progress).execute_query()

print(f"✅ {uploaded.server_relative_url} uploaded")
