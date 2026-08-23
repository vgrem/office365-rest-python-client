"""
Recycle bin — list deleted items, restore, and permanently delete.

Items deleted from OneDrive/SharePoint go to the recycle bin first. This
example shows how to:
  - List deleted items in the recycle bin
  - Restore a deleted file back to its original location
  - Permanently delete (purge) an item without recovery

Compliance teams use this for data retention and eDiscovery workflows.

Requires delegated permission ``Files.ReadWrite.All`` (and ``Sites.ReadWrite.All``
for SharePoint document libraries).

https://learn.microsoft.com/en-us/graph/api/resources/recyclebin
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List, restore and purge recycle bin items")
    parser.add_argument("--purge", action="store_true", help="permanently delete the first item (no recovery)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    drive = client.me.drive
    recycle = drive.recycle_bin

    # -- Step 1: create a throwaway file so there is something in the bin --
    root = drive.root
    test_file = root.get_by_path("recycle_bin_demo.txt")
    try:
        test_file.get().execute_query()
    except Exception:
        root.upload("recycle_bin_demo.txt", b"Delete me.").execute_query()
    test_file.delete_object().execute_query()
    print("Uploaded and deleted 'recycle_bin_demo.txt' (now in the recycle bin)\n")

    # -- Step 2: list deleted items --
    items = recycle.items.get().execute_query()
    print(f"Recycle bin items ({len(items)}):")
    for item in items:
        deleted = item.deleted_date_time
        deleted_str = deleted.strftime("%Y-%m-%d %H:%M") if deleted else "?"
        print(f"  {item.name:40s}  deleted: {deleted_str}")

    # -- Step 3: restore the first item --
    drive_id = drive.properties.get("id")
    if items and drive_id and items[0].id:
        target = items[0]
        target_id = target.id
        if target_id:
            print(f"\nRestoring '{target.name}'...")
            client.drives[drive_id].items[target_id].restore().execute_query()
            print("  ✓ Restored to its original location")

    # -- Step 4: permanently delete the first item (optional) --
    if args.purge:
        items = recycle.items.get().execute_query()
        if items and drive_id and items[0].id:
            target = items[0]
            target_id = target.id
            if target_id:
                print(f"\nPurging '{target.name}' permanently...")
                client.drives[drive_id].items[target_id].permanent_delete().execute_query()
                print("  ✓ Permanently deleted (not recoverable)")


if __name__ == "__main__":
    main()
