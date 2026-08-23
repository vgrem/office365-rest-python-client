"""
Download a folder tree as a zip file.

Streams every file inside the folder (including subfolders) into a single zip
archive with ``download_folder()``.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-get-content
"""

import argparse
import os
import tempfile
import zipfile

from office365.graph_client import GraphClient
from office365.onedrive.driveitems.driveItem import DriveItem
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def _downloaded(file: DriveItem) -> None:
    print(f"  ✓ {file.name}")


def main():
    parser = argparse.ArgumentParser(description="Download a folder as a zip file")
    parser.add_argument("--keep", action="store_true", help="keep the folder after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- Step 1: create a small folder tree with files --
    root = client.me.drive.root
    folder = root.create_folder(create_unique_name("download")).execute_query()
    folder.upload("one.txt", b"1\n").execute_query()
    sub = folder.create_folder("nested").execute_query()
    sub.upload("two.txt", b"2\n").execute_query()
    print(f"Created test tree under '{folder.name}'\n")

    # -- Step 2: download the whole tree as a zip --
    zip_path = os.path.join(tempfile.gettempdir(), f"{folder.name}.zip")
    with open(zip_path, "wb") as to_file:
        folder.download_folder(to_file, _downloaded).execute_query()

    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
    print(f"\nZipped {len(names)} file(s) into: {zip_path}")
    for name in names:
        print(f"  {name}")

    if not args.keep:
        folder.delete_object().execute_query()
        print("\nFolder removed.")


if __name__ == "__main__":
    main()
