"""
List item CRUD — create, read, update, and delete items.

The day-to-day pattern for working with data inside a SharePoint list:
create items with column values, read them back, update fields, and clean up.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/listitem-create
https://learn.microsoft.com/en-us/graph/api/listitem-update
https://learn.microsoft.com/en-us/graph/api/listitem-delete
"""

import argparse

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Create, read, update and delete list items")
    parser.add_argument("--keep", action="store_true", help="keep the list after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create a list with a text column --
    lib = site.lists.add(create_unique_name("Orders"), ListTemplateType.genericList).execute_query()
    lib.columns.add_text("Category").execute_query()
    print(f"List: '{lib.display_name}'")

    # -- Step 2: create items --
    first = lib.items.add(Title="Q4 Report", Category="Finance").execute_query()
    second = lib.items.add(Title="Q1 Forecast", Category="Sales").execute_query()
    print(f"  Created items: '{first.name}' (id={first.id}), '{second.name}' (id={second.id})")

    # -- Step 3: read items back with their column values --
    items = lib.items.expand(["fields"]).get().execute_query()
    print(f"\nItems ({len(items)}):")
    for item in items:
        category = item.fields.get_property("Category") or "?"
        print(f"  {item.name:20s}  category: {category}")

    # -- Step 4: update an item --
    first.set_property("Category", "Operations").update().execute_query()
    print("\n  ✓ Updated first item's Category to 'Operations'")

    # -- Step 5: delete an item --
    second.delete_object().execute_query()
    print("  ✓ Deleted second item")

    if not args.keep:
        lib.delete_object().execute_query()
        print("\nList removed.")


if __name__ == "__main__":
    main()
