"""
Create a nested folder structure in one go.

Builds a year / quarter / report tree (e.g. ``2024/Q1/Reports``) using a small
helper that creates each missing level along the path — a common way to set up
an archive or document structure.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-post-children
"""

import argparse

from office365.graph_client import GraphClient
from office365.onedrive.driveitems.driveItem import DriveItem
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def _ensure_folder(parent: DriveItem, name: str) -> DriveItem:
    """Create a folder if it doesn't exist and return it."""
    try:
        return parent.get_by_path(name).get().execute_query()
    except Exception:
        return parent.create_folder(name).execute_query()


def main():
    parser = argparse.ArgumentParser(description="Create a nested folder structure")
    parser.add_argument("--keep", action="store_true", help="keep the folders after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- build 2024/Q1/Reports under a unique root folder --
    root_name = create_unique_name("Archive")
    root = client.me.drive.root.create_folder(root_name).execute_query()
    year = _ensure_folder(root, "2024")
    quarter = _ensure_folder(year, "Q1")
    _ensure_folder(quarter, "Reports")

    # -- print the resulting tree --
    print(f"Created under '{root.name}':")
    for child in root.children.get().execute_query():
        print(f"  {child.name}/")
        for sub in child.children.get().execute_query():
            print(f"    {sub.name}/")
            for leaf in sub.children.get().execute_query():
                print(f"      {leaf.name}/")

    if not args.keep:
        root.delete_object().execute_query()
        print("\nFolder tree removed.")


if __name__ == "__main__":
    main()
