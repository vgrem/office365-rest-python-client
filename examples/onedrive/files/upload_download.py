"""
Upload a file to OneDrive, then download it back and verify the round-trip.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-put-content
https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
"""

import argparse
import os
import tempfile

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upload a file to OneDrive and download it back")
    parser.add_argument("--path", help="path to the local file to upload (default: a generated sample)")
    parser.add_argument("--keep", action="store_true", help="keep the uploaded file after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    if args.path:
        local_path = args.path
    else:
        local_path = os.path.join(tempfile.gettempdir(), "sample.txt")
        with open(local_path, "w", encoding="utf-8") as f:
            f.write("Hello from office365-rest-python-client\n" * 100)

    name = os.path.basename(local_path)
    uploaded = client.me.drive.root.upload_file(local_path).execute_query()
    print(f"Uploaded '{name}' ({uploaded.size or 0:,} bytes)")

    download_path = os.path.join(tempfile.gettempdir(), create_unique_name("download") + name)
    with open(download_path, "wb") as f:
        uploaded.download(f).execute_query()

    same_size = os.path.getsize(local_path) == os.path.getsize(download_path)
    print(f"Downloaded to: {download_path}  ({os.path.getsize(download_path):,} bytes)")
    print(f"Round-trip OK: {same_size}")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("Uploaded file removed.")


if __name__ == "__main__":
    main()
