"""
Delete a list item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete a list item")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--item-id", type=int, required=True, help="item id to delete")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    item.delete_object().execute_query()
    print(f"Deleted item {args.item_id}")


if __name__ == "__main__":
    main()
