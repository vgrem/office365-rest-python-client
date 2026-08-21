"""
Update one or more fields on a list item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Update a list item")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--item-id", type=int, required=True, help="item id to update")
    parser.add_argument("--title", default="Updated title", help="new title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    item.set_property("Title", args.title).update().execute_query()
    print(f"Updated item {args.item_id}")


if __name__ == "__main__":
    main()
