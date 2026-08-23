"""
Largest files report — top storage consumers in a drive.

Walks the drive tree recursively and lists the biggest files, useful for
storage triage and cleanup decisions.

Requires delegated permission ``Files.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-list-children
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

GIB = 1024**3


def main():
    parser = argparse.ArgumentParser(description="Report the largest files in your drive")
    parser.add_argument("--top", type=int, default=20, help="how many largest files to show (default: 20)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    files = client.me.drive.root.get_files(recursive=True).execute_query()

    largest = sorted((f for f in files if f.size), key=lambda f: f.size or 0, reverse=True)[: args.top]
    total = sum(f.size or 0 for f in files)

    print(f"{len(files):,} files, {total / GIB:.2f} GiB total\n")
    print("Largest files:")
    for f in largest:
        size = f.size or 0
        print(f"  {size / GIB:8.2f} GiB  {f.name}")


if __name__ == "__main__":
    main()
