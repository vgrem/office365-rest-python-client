"""
Set a lookup field value on a list item (reference another list's item).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.lookup_value import FieldLookupValue
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Set a lookup field on a list item")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    parser.add_argument("--item-id", type=int, required=True, help="item id to update")
    parser.add_argument("--field", default="Project", help="lookup field internal name")
    parser.add_argument("--lookup-item-id", type=int, required=True, help="id of the referenced item")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    item.set_property(args.field, FieldLookupValue(LookupId=args.lookup_item_id)).update().execute_query()
    print(f"Set lookup {args.field} on item {args.item_id} -> {args.lookup_item_id}")


if __name__ == "__main__":
    main()
