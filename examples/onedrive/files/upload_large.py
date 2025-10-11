"""
Demonstrates how to upload a large file

https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
chunk_size = 1 * 1024 * 1024
local_path = "../../../tests/data/big_buck_bunny.mp4"
remote_folder = client.me.drive.root.get_by_path("archive")
remote_file = (
    remote_folder.resumable_upload(
        local_path,
        chunk_size=chunk_size,
        chunk_uploaded=lambda range_pos: print(f"{range_pos} bytes uploaded"),
    )
    .get()
    .execute_query()
)
print(f"File {remote_file.web_url} has been uploaded")
