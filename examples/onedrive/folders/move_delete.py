"""
Rename, move, and delete folders.

Shows how folders are relocated (the same ``move()`` used for files) and how
deleting a folder removes its whole subtree into the recycle bin.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-update
https://learn.microsoft.com/en-us/graph/api/driveitem-delete
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Rename, move and delete folders")
    parser.add_argument("--keep", action="store_true", help="keep the folders after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    root = client.me.drive.root

    # -- Step 1: create a folder and rename it --
    folder = root.create_folder(create_unique_name("Original")).execute_query()
    renamed = folder.rename(create_unique_name("Renamed")).execute_query()
    print(f"Renamed to: '{renamed.name}'")

    # -- Step 2: move it into a new parent folder --
    parent = root.create_folder(create_unique_name("Parent")).execute_query()
    moved = renamed.move(name=renamed.name, parent=parent).execute_query()
    print(f"Moved into '{parent.name}'")

    # -- Step 3: confirm the move by listing the parent --
    children = parent.children.get().execute_query()
    print(f"  '{parent.name}' now contains: {[c.name for c in children]}")

    # -- Step 4: delete the folder tree (goes to the recycle bin) --
    if not args.keep:
        moved.delete_object().execute_query()
        parent.delete_object().execute_query()
        print("\nFolders removed (recoverable from the recycle bin).")


if __name__ == "__main__":
    main()
