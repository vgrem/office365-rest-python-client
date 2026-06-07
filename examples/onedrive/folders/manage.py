"""
Create folders, navigate the hierarchy, and list contents.

Folders organize files in OneDrive. This shows the common
patterns for working with the folder tree.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-post-children
https://learn.microsoft.com/en-us/graph/api/driveitem-list-children
https://learn.microsoft.com/en-us/graph/api/driveitem-get
"""

import uuid

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# 1. Create a folder
folder_name = f"Project_{uuid.uuid4().hex[:8]}"
folder = client.me.drive.root.create_folder(folder_name).execute_query()
print(f"Folder created: {folder.name}  (id: {folder.id})")

# 2. Create a subfolder inside it
sub = folder.create_folder("Reports").execute_query()
print(f"  Subfolder: {sub.name}")

# 3. Upload a file into the folder
uploaded = folder.upload("notes.txt", b"Project notes").execute_query()
print(f"  File uploaded: {uploaded.name}")

# 4. List folder contents
children = folder.children.get().execute_query()
print(f"\nContents of '{folder_name}' ({len(children)} items):")
for child in children:
    print(f"  {'📄' if child.is_file else '📁'}  {child.name}  ({child.size or 0:,} bytes)")
