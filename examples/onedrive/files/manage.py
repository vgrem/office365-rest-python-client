"""
File operations: copy, move, rename, delete, and view versions.

Common file management tasks once a file is on OneDrive.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-copy
https://learn.microsoft.com/en-us/graph/api/driveitem-update
https://learn.microsoft.com/en-us/graph/api/driveitem-delete
https://learn.microsoft.com/en-us/graph/api/driveitem-list-versions
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

item = client.me.drive.root.children.top(1).get().execute_query()
if len(item) == 0:
    exit("No files found. Upload a file first.")

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
