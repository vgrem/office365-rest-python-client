"""
File operations — copy, rename, move, list versions, and delete.

The common file management tasks once a file is on OneDrive, demonstrated
end-to-end on a throwaway file so it is safe to re-run.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-copy
https://learn.microsoft.com/en-us/graph/api/driveitem-update
https://learn.microsoft.com/en-us/graph/api/driveitem-delete
https://learn.microsoft.com/en-us/graph/api/driveitem-list-versions
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Copy, rename, move, version and delete a file")
    parser.add_argument("--keep", action="store_true", help="keep the test file after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    root = client.me.drive.root

    # -- Step 1: create a test file --
    name = create_unique_name("file_ops") + ".txt"
    item = root.upload(name, b"Version 1\n").execute_query()
    print(f"Created: {item.name}")

    # -- Step 2: copy (async — returns a location, then resolve the new item) --
    item.copy(f"Copy_of_{item.name}").execute_query()
    copy = root.get_by_path(f"Copy_of_{name}").get().execute_query()
    print(f"  ✓ Copied as: {copy.name}")

    # -- Step 3: rename --
    renamed = item.rename(f"renamed_{item.name}").execute_query()
    print(f"  ✓ Renamed to: {renamed.name}")

    # -- Step 4: update content (creates a new version) --
    renamed.upload(f"renamed_{name}", b"Version 1\nVersion 2\n").execute_query()
    print("  ✓ Uploaded new content (new version created)")

    # -- Step 5: list versions --
    versions = renamed.versions.get().execute_query()
    print(f"  ✓ Version history ({len(versions)} versions)")
    for v in versions:
        dt = v.get_property("lastModifiedDateTime")
        dt = dt.strftime("%Y-%m-%d %H:%M") if dt else "?"
        label = v.get_property("label") or "?"
        print(f"      v{label}  {dt}")

    # -- Step 6: move to a folder --
    folder = root.create_folder(create_unique_name("folder")).execute_query()
    moved = renamed.move(name=renamed.name, parent=folder).execute_query()
    print(f"  ✓ Moved into '{folder.name}'")

    # -- Step 7: delete (soft delete — goes to the recycle bin) --
    copy.delete_object().execute_query()
    if not args.keep:
        moved.delete_object().execute_query()
        folder.delete_object().execute_query()
        print("  ✓ Test items deleted (recoverable from recycle bin)")


if __name__ == "__main__":
    main()
