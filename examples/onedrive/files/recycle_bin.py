"""
Recycle bin — list deleted items, restore, and permanently delete.

Items deleted from OneDrive/SharePoint go to the recycle bin first.
This example shows how to:
  - List deleted items in the recycle bin
  - Restore a deleted file back to its original location
  - Permanently delete (purge) an item without recovery

Compliance teams use this for data retention and eDiscovery workflows.

Requires delegated permission ``Files.ReadWrite.All`` and
``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/recyclebin
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    # -- Step 1: access the recycle bin --
    # The recycle bin is a property on the drive.
    # For OneDrive: client.me.drive.recycle_bin
    # For SharePoint: client.sites["{site-id}"].drive.recycle_bin

    drive = client.me.drive
    recycle = drive.recycle_bin  # This returns a RecycleBin entity

    # -- Step 2: list deleted items --
    # Items in the recycle bin are accessible via `recycle.items`
    # (but note: this is read from a Collection navigation property)
    try:
        items = recycle.items.get().execute_query()
    except AttributeError:
        # Fallback: some SDK versions expose it differently
        print("(recycle_bin.items not directly available — checking alternate path)\n")

        # Delete a test file so there's something in the bin
        root = drive.root.get().execute_query()
        test_file = root.get_by_path("recycle_bin_test.txt")
        try:
            exists = test_file.get().execute_query()
            print(f"Deleting existing test file: {exists.name}")
            exists.delete_object().execute_query()
        except Exception:
            root.upload("recycle_bin_test.txt", b"Content to be deleted").execute_query()
            test_file.get().execute_query()
            test_file.delete_object().execute_query()

        print("Test file deleted to recycle bin.\n")
        print("Recycle bin items can be accessed via the drive's recycleBin.")
        print("See Graph API docs for the exact endpoint:\n")
        print(f"  GET /drives/{drive.properties.get('id', '?')}/recycleBin/items\n")
        return

    if len(items) == 0:
        print("Recycle bin is empty.\n")

        # Create a test file, delete it, then show it
        root = drive.root.get().execute_query()
        test_file = root.upload("recycle_bin_test.txt", b"Temporary content.").execute_query()
        print(f"Created test file: {test_file.name}")

        test_file.delete_object().execute_query()
        print("Deleted — now in the recycle bin.\n")

        # Reload
        items = recycle.items.get().execute_query()

    print(f"Recycle bin items ({len(items)}):\n")
    for item in items:
        deleted_dt = item.properties.get("deletedDateTime", item.properties.get("deleted", None))
        if hasattr(deleted_dt, "strftime"):
            deleted_dt = deleted_dt.strftime("%Y-%m-%d %H:%M")
        original = item.properties.get("name", "?")
        size = item.properties.get("size", "?")
        print(f"  {original:35s}  size={size:>8}  deleted={deleted_dt or '?'}")

    # -- Step 3: restore the first item from the bin --
    if items:
        print("\nRestoring the first item...")
        item = items[0]
        try:
            item.restore().execute_query()
            print(f"  ✓ Restored: {item.properties.get('name', '?')}")
        except Exception as e:
            print(f"  Restore not available: {e}")

    # -- Step 4: permanent delete a specific item (commented out) --
    # Permanent delete bypasses the bin entirely:
    #   item.permanent_delete().execute_query()
    #
    # Or permanently purge from recycle bin:
    #   recycle.items["<item-id>"].permanent_delete().execute_query()


if __name__ == "__main__":
    main()
