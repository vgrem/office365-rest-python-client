"""
Upload a local folder tree to OneDrive.

Mirrors the local directory structure (files and subfolders) under a target
folder using the recursive ``upload_folder()`` helper.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-put-content
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username

LOCAL_FOLDER = Path(__file__).resolve().parents[2] / "data" / "reports"


def main():
    parser = argparse.ArgumentParser(description="Upload a local folder tree to OneDrive")
    parser.add_argument("--path", help="path to the local folder (default: examples/data/reports)")
    parser.add_argument("--keep", action="store_true", help="keep the uploaded folder after the demo")
    args = parser.parse_args()

    local_path = Path(args.path) if args.path else LOCAL_FOLDER
    if not local_path.is_dir():
        parser.error(f"Not a directory: {local_path}")

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    target = client.me.drive.root.create_folder(create_unique_name("upload")).execute_query()

    def _uploaded(item) -> None:
        print(f"  ✓ {item.name}")

    target.upload_folder(str(local_path), _uploaded).execute_query()
    print(f"\nUploaded '{local_path.name}' to '{target.name}'")

    if not args.keep:
        target.delete_object().execute_query()
        print("Uploaded folder removed.")


if __name__ == "__main__":
    main()
