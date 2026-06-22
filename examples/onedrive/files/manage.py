"""
File operations: copy, move, rename, delete, and view versions.

Common file management tasks once a file is on OneDrive.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-copy
https://learn.microsoft.com/en-us/graph/api/driveitem-update
https://learn.microsoft.com/en-us/graph/api/driveitem-delete
https://learn.microsoft.com/en-us/graph/api/driveitem-list-versions
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

item = client.me.drive.root.children.top(1).get().execute_query()
if len(item) == 0:
    sys.exit("No files found. Upload a file first.")

file = item[0]
print(f"Working with: {file.name}  (id: {file.id})")

# 1. Copy
copy = file.copy(f"Copy_of_{file.name}").execute_query()
print(f"  ✓ Copied as: Copy_of_{file.name}")

# 2. Rename
file.rename(f"renamed_{file.name}").execute_query()
print(f"  ✓ Renamed to: renamed_{file.name}")

# 3. List versions
versions = file.versions.get().execute_query()
print(f"  ✓ Versions: {len(versions)}")
