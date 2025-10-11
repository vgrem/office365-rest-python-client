"""
Example demonstrates how to download OneDrive files into local file system

https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/driveitem_get_content?view=odsp-graph-online
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_tenant,
    test_user_principal_name,
)

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)
drive = client.users[test_user_principal_name].drive
with tempfile.TemporaryDirectory() as local_path:
    drive_items = drive.root.children.get().execute_query()
    file_items = [item for item in drive_items if item.file is not None]
    for drive_item in file_items:
        with open(os.path.join(local_path, drive_item.name), "wb") as local_file:
            drive_item.download(local_file).execute_query()
        print(f"File '{local_file.name}' has been downloaded")
