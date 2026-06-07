"""
Upload a file to OneDrive, then download it.

The most common file operation — upload and download content.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-put-content
https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# Upload a file to OneDrive root
content = b"Hello, OneDrive!"
uploaded = client.me.drive.root.upload("hello.txt", content).execute_query()
print(f"Uploaded: {uploaded.name}  (id: {uploaded.id})")

# Download it back
with tempfile.TemporaryDirectory() as path:
    local_path = os.path.join(path, "hello.txt")
    with open(local_path, "wb") as f:
        uploaded.download(f).execute_query()
    print(f"Downloaded to: {local_path}  (size: {os.path.getsize(local_path)} bytes)")
