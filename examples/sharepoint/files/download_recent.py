"""
Demonstrates how to download the most recently uploaded file from a document library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
lib_title = "Documents"
lib = ctx.web.lists.get_by_title(lib_title)

recent_items = lib.items.order_by("Created desc").select(["ID", "FileRef"]).top(1).get().execute_query()
for item in recent_items:
    file_url = item.properties.get("FileRef")
    download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
    with open(download_path, "wb") as local_file:
        item.file.download(local_file).execute_query()
    print(f"[Ok] file has been downloaded into: {download_path}")
