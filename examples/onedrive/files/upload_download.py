"""
Upload a file to OneDrive, then download it back.

Requires delegated permission Files.ReadWrite.
"""

from pathlib import Path

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

file_name = "Financial Sample.xlsx"
local_path = Path("../../data") / file_name

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

uploaded = client.me.drive.root.upload_file(local_path).execute_query()

download_path = Path(__file__).parent / file_name
with open(download_path, "wb") as f:
    uploaded.download(f).execute_query()

print(f"Uploaded and downloaded: {file_name}  ({download_path.stat().st_size:,} bytes)")
