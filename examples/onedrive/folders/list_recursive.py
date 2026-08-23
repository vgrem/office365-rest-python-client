"""
Recursively list all files and folders in the drive.

Walks the whole hierarchy with ``get_files()`` / ``get_folders()`` and reports
a flat inventory — useful for audits, migrations, or quota reporting.

Requires delegated permission ``Files.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-list-children
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List all files and folders recursively")
    parser.add_argument("--folder", default="/", help="path to start from (default: drive root)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    root = client.me.drive.root.get_by_path(args.folder).get().execute_query()

    folders = root.get_folders(recursive=True).execute_query()
    files = root.get_files(recursive=True).execute_query()

    total_size = sum(f.size or 0 for f in files)
    print(f"Under '{args.folder}':")
    print(f"  {len(folders):,} folders, {len(files):,} files ({total_size:,} bytes total)\n")

    print("Files (first 25):")
    for f in list(files)[:25]:
        print(f"  {f.name:40s}  {f.size or 0:,} bytes")


if __name__ == "__main__":
    main()
