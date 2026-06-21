"""
Mail folder management: create, navigate, empty, mark all read, and
permanent-delete folders.

Mailbox cleanup and compliance workflows often need bulk operations
on folders — purge old content, reset unread counts, or remove
stale folder trees.

Requires delegated permission ``Mail.ReadWrite`` and
``MailboxSettings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/mailfolder
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def walk_folders(client: GraphClient, parent_path="inbox", indent=0):
    """Recursively list folders and subfolders with item counts."""
    parent = client.me.mail_folders[parent_path]
    parent.select(["displayName", "totalItemCount", "unreadItemCount"]).expand(["childFolders"]).execute_query()

    prefix = "  " * indent
    print(
        f"{prefix}{parent.display_name}  ({parent.total_item_count or 0} items, {parent.unread_item_count or 0} unread)"
    )

    if parent.child_folders:
        for child in parent.child_folders:
            walk_folders(client, child.id, indent + 1)


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- Step 1: create a folder --
    inbox = client.me.mail_folders["inbox"]
    new_folder = inbox.child_folders.add("Cleanup Test").execute_query()
    print(f"Created folder: '{new_folder.display_name}' (id: {new_folder.id})")

    # -- Step 2: create a child subfolder --
    sub_folder = new_folder.child_folders.add("Subfolder").execute_query()
    print(f"Created subfolder: '{sub_folder.display_name}'")

    # -- Step 3: navigate the tree --
    print("\nMailbox folder tree:")
    walk_folders(client)
    print()

    # -- Step 4: mark all items as read in a folder --
    # Move one message into the folder first so we have something
    latest = client.me.mail_folders["inbox"].messages.top(1).get().execute_query()
    if latest:
        latest[0].move(new_folder.id).execute_query()
        print("Moved 1 message into folder (to simulate unread).")

    new_folder.mark_all_items_as_read().execute_query()
    print(f"✓ Marked all items as read in '{new_folder.display_name}'.")

    # -- Step 5: empty the folder (delete all items) --
    new_folder.empty(delete_sub_folders=True).execute_query()
    print(f"✓ Emptied '{new_folder.display_name}' (including subfolders).")

    # -- Step 6: permanent delete removes the folder itself --
    # Re-fetch the folder reference
    target = client.me.mail_folders[new_folder.id]
    target.permanent_delete().execute_query()
    print("✓ Permanent-deleted the folder.")

    # Verify it's gone
    try:
        client.me.mail_folders[new_folder.id].get().execute_query()
    except Exception:
        print("  Confirmed: folder no longer exists.")


if __name__ == "__main__":
    main()
