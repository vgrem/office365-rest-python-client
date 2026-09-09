"""
Create a nested folder structure in one call.

Builds ``2024/Q1/Reports`` under a unique root folder with the deferred
``DriveItem.ensure_folder(path)`` — each missing level is created along the
path and the whole chain runs on a single ``execute_query()``.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-post-children
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a nested folder structure")
    parser.add_argument("--keep", action="store_true", help="keep the folders after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    root_name = create_unique_name("Archive")
    root = client.me.drive.root.create_folder(root_name).execute_query()
    reports = root.ensure_folder("2024/Q1/Reports").execute_query()
    print(f"Created '{reports.name}' under '{root.name}'")

    # Resolve the same path again to confirm it now exists
    same = root.get_by_path("2024/Q1/Reports").get().execute_query()
    print(f"Resolved again: {same.name} (id: {same.id})")

    if not args.keep:
        root.delete_object().execute_query()
        print("Folder tree removed.")


if __name__ == "__main__":
    main()
