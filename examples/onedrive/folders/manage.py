"""
Create folders, navigate the hierarchy, and list contents.

The basic folder lifecycle: create a folder and a subfolder, upload a file,
and list the children.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-post-children
https://learn.microsoft.com/en-us/graph/api/driveitem-list-children
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create folders and list their contents")
    parser.add_argument("--keep", action="store_true", help="keep the folder after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- Step 1: create a folder --
    folder = client.me.drive.root.create_folder(create_unique_name("Project")).execute_query()
    print(f"Folder created: '{folder.name}'  (id: {folder.id})")

    # -- Step 2: create a subfolder inside it --
    sub = folder.create_folder("Reports").execute_query()
    print(f"  Subfolder: {sub.name}")

    # -- Step 3: upload a file into the folder --
    uploaded = folder.upload("notes.txt", b"Project notes\n").execute_query()
    print(f"  File uploaded: {uploaded.name}")

    # -- Step 4: list contents --
    children = folder.children.get().execute_query()
    print(f"\nContents of '{folder.name}' ({len(children)} items):")
    for child in children:
        kind = "folder" if child.is_folder else "file"
        print(f"  {child.name:25s}  {kind:6s}  {child.size or 0:,} bytes")

    if not args.keep:
        folder.delete_object().execute_query()
        print("\nFolder removed (recoverable from the recycle bin).")


if __name__ == "__main__":
    main()
