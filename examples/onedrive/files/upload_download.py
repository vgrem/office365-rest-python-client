"""
Upload a file to OneDrive, then download it back.

Requires delegated permission Files.ReadWrite.
"""

from pathlib import Path

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

FILE_NAME = "Financial Sample.xlsx"
LOCAL_PATH = Path("../../data") / FILE_NAME

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

with open(LOCAL_PATH, "rb") as f:
    uploaded = client.me.drive.root.upload_file(f).execute_query()

download_path = Path(__file__).parent / FILE_NAME
with open(download_path, "wb") as f:
    uploaded.download(f).execute_query()

print(f"Uploaded and downloaded: {FILE_NAME}  ({download_path.stat().st_size:,} bytes)")
