"""
Demonstrates how to download the most recently uploaded file from a document library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Download the most recent file in a library")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lib = ctx.web.lists.get_by_title(args.list_title)

    items = lib.items.order_by("Created desc").select(["ID", "FileRef"]).top(1).get().execute_query()
    if not items:
        print("No items found in the library.")
        return

    item = items[0]
    file_name = item.file.name or "download.bin"
    download_path = os.path.join(tempfile.mkdtemp(), file_name)
    with open(download_path, "wb") as local_file:
        item.file.download(local_file).execute_query()
    print(f"[Ok] file has been downloaded into: {download_path}")


if __name__ == "__main__":
    main()
