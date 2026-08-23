"""
Search files and folders in your OneDrive by keyword.

Requires delegated permission ``Files.Read``.

https://learn.microsoft.com/en-us/graph/api/driveitem-search
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Search OneDrive by keyword")
    parser.add_argument("--query", required=True, help="search query, e.g. 'report'")
    parser.add_argument("--top", type=int, default=50, help="max results to show (default: 50)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    results = client.me.drive.search(args.query).top(args.top).get().execute_query()

    print(f"Found {len(results)} items matching '{args.query}':")
    for item in results:
        kind = "file" if item.is_file else "folder"
        print(f"  {item.name:45s}  {kind:6s}  {item.size or 0:,} bytes")


if __name__ == "__main__":
    main()
