"""
Read the resolved value of a lookup field on a list item.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get a lookup field value")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    parser.add_argument("--item-id", type=int, required=True, help="item id")
    parser.add_argument("--field", default="Project", help="lookup field internal name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    item.expand([args.field]).get().execute_query()
    value = item.properties.get(args.field)
    print(f"{args.field}: {value}")


if __name__ == "__main__":
    main()
