"""
Read list items including specific fields via $select.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Read list items with selected fields")
    parser.add_argument("--list-title", default="Documents", help="list title")
    parser.add_argument("--fields", nargs="+", default=["Title", "Created", "Modified"], help="fields to select")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    items = ctx.web.lists.get_by_title(args.list_title).items.select(args.fields).get().execute_query()
    print(f"Items ({len(items)}):")
    for item in items:
        values = ", ".join(f"{f}={item.properties.get(f, '?')}" for f in args.fields)
        print(f"  {item.id}: {values}")


if __name__ == "__main__":
    main()
