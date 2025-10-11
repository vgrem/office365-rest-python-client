"""
Download the contents of the driveItem (folder facet)

https://learn.microsoft.com/en-us/graph/api/driveitem-get-content?view=graph-rest-1.0
"""

import os
import tempfile

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
folder_item = client.me.drive.root.get_by_path("archive").get().execute_query()

with tempfile.TemporaryDirectory() as local_path:
    items = folder_item.children.get().execute_query()
    for drive_item in items:
        if drive_item.is_file:
            with open(os.path.join(local_path, drive_item.name), "wb") as local_file:
                drive_item.download(local_file).execute_query()  # download file content
            print(f"File '{drive_item.name}' has been downloaded into {local_file.name}")
