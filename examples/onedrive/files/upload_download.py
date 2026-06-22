"""
Upload a file to OneDrive, then download it back.

Requires delegated permission Files.ReadWrite.
"""

import os
import tempfile
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

file_name = "Financial Sample.xlsx"
local_path = Path("../../data") / file_name

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

uploaded = client.me.drive.root.upload_file(local_path).execute_query()

download_path = os.path.join(tempfile.gettempdir(), file_name)
with open(download_path, "wb") as f:
    uploaded.download(f).execute_query()

print(f"Uploaded and downloaded: {file_name}  ({os.path.getsize(download_path):,} bytes)")
