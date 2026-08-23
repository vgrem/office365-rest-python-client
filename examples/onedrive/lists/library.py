"""
Document library operations — upload, download, and organize files.

A document library is a list that also acts as a drive: you can manage files
and folders with the same DriveItem API used for OneDrive.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/driveitem-put-content
https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
"""

import argparse
import io

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Upload, organize and download files in a document library")
    parser.add_argument("--keep", action="store_true", help="keep the library after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create a document library --
    lib = site.lists.add(create_unique_name("Assets"), ListTemplateType.documentLibrary).execute_query()
    root = lib.drive.root.get().execute_query()
    print(f"Document library: '{lib.display_name}'\n")

    # -- Step 2: upload files and create a folder --
    root.upload("readme.txt", b"Hello from the Assets library\n").execute_query()
    root.upload("budget.csv", b"year,amount\n2024,120000\n").execute_query()
    folder = root.create_folder("2024").execute_query()
    folder.upload("report.txt", b"Annual report\n").execute_query()
    print("  ✓ Uploaded readme.txt, budget.csv; created folder '2024' with report.txt")

    # -- Step 3: list contents --
    children = root.children.get().execute_query()
    print(f"\nContents of '{lib.display_name}' ({len(children)} items):")
    for child in children:
        kind = "folder" if child.is_folder else "file"
        print(f"  {child.name:20s}  {kind:6s}  {child.size or 0:,} bytes")

    # -- Step 4: download a file --
    file_item = root.get_by_path("budget.csv").get().execute_query()
    buffer = io.BytesIO()
    file_item.download(buffer).execute_query()
    content = buffer.getvalue().decode("utf-8")
    print(f"\nDownloaded 'budget.csv' ({len(content)} bytes):")
    print(content)

    if not args.keep:
        lib.delete_object().execute_query()
        print("Library removed.")


if __name__ == "__main__":
    main()
