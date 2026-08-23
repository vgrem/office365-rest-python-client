"""
Download and read a JSON file from OneDrive.

Uploads a small JSON document, downloads it via ``get_content()``, parses it back
with ``json.loads``, and prints the contents.

A ``.json`` file is served by the OneDrive ``/content`` endpoint with
``Content-Type: application/json``, so without the raw-content handling this used
to fail (the client tried to parse the file as an OData response).

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
"""

import argparse
import json
import os
import tempfile

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username

sample = {
    "name": "office365-rest-python-client",
    "version": 1,
    "features": ["graph", "sharepoint"],
    "active": True,
}


def main():
    parser = argparse.ArgumentParser(description="Download and read a JSON file from OneDrive")
    parser.add_argument("--keep", action="store_true", help="keep the uploaded file after downloading")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # 1. Upload a JSON file
    name = create_unique_name("sample") + ".json"
    local_path = os.path.join(tempfile.gettempdir(), name)
    with open(local_path, "w", encoding="utf-8") as f:
        json.dump(sample, f)

    uploaded = client.me.drive.root.upload_file(local_path).execute_query()
    os.remove(local_path)
    print(f"Uploaded '{uploaded.name}'")

    # 2. Download it back as raw bytes and parse as JSON
    content = uploaded.get_content().execute_query()
    parsed = json.loads(content.value)
    print(f"Downloaded {len(content.value):,} bytes")
    print(f"Parsed JSON: {json.dumps(parsed, indent=2)}")
    assert parsed == sample

    # 3. Clean up
    if not args.keep:
        uploaded.delete_object().execute_query()
        print("Uploaded file removed.")


if __name__ == "__main__":
    main()
