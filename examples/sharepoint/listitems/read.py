"""
Read all items from a list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Read list items")
    parser.add_argument("--list-title", default="Documents", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    items = ctx.web.lists.get_by_title(args.list_title).items.get().execute_query()
    print(f"Items ({len(items)}):")
    for item in items:
        print(f"  {item.id}: {item.properties.get('Title', '?')}")


if __name__ == "__main__":
    main()
