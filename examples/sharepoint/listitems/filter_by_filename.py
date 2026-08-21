"""
Filter items in a document library by file name.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Filter documents by file name")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    parser.add_argument("--name", default="report", help="file name (or substring) to match")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    items = (
        ctx.web.lists.get_by_title(args.list_title)
        .items.filter(f"substringof('{args.name}', FileLeafRef)")
        .get()
        .execute_query()
    )
    print(f"Files matching '{args.name}' ({len(items)}):")
    for item in items:
        print(f"  {item.properties.get('FileLeafRef', '?')}")


if __name__ == "__main__":
    main()
