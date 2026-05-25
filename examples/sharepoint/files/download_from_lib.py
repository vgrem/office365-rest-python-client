"""
Demonstrates how to download files from a SharePoint library.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import tempfile
from pathlib import Path

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

doc_lib = ctx.web.lists.get_by_title("Documents")
items = (
    doc_lib.items.select(["FileSystemObjectType"])
    .select(["Id", "FileRef", "FileDirRef", "FileLeafRef"])
    .filter("FSObjType eq 0")
    .get_all()
    .execute_query()
)

download_root_path = Path(tempfile.mkdtemp())

for item in items:
    dir_ref = item.properties.get("FileDirRef")
    assert dir_ref is not None
    download_path = download_root_path / dir_ref.lstrip("/")
    download_path.mkdir(parents=True, exist_ok=True)

    leaf_ref = item.properties.get("FileLeafRef")
    assert leaf_ref is not None
    download_file_path = download_path / leaf_ref

    with open(download_file_path, "wb") as f:
        item.file.download(f).execute_query()
        print(f"File has been downloaded into {f.name}")
