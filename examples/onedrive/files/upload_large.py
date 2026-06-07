"""
Upload a large file using a resumable upload session.

Files larger than ~4 MB should use the resumable upload session.
The SDK handles chunked upload automatically.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# Create a 5 MB file in memory
content = b"A" * 5_000_000
uploaded = client.me.drive.root.upload("large_file.bin", content).execute_query()
print(f"Uploaded: {uploaded.name}  ({len(content)} bytes)")
print(f"Web URL: {uploaded.web_url}")
