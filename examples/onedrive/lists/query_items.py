"""
Query list items — filter, select, order, and page.

How to read data out of a list efficiently: limit columns with ``$select``,
filter rows with ``$filter``, sort with ``$orderby``, and control page size.
The same query options work on any collection in the SDK.

Requires delegated permission ``Sites.Read.All`` or ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/listitem-list
"""

import argparse

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Query list items with filter, select and order")
    parser.add_argument("--keep", action="store_true", help="keep the list after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create a list with sample data --
    lib = site.lists.add(create_unique_name("Projects"), ListTemplateType.genericList).execute_query()
    lib.columns.add_number("Budget").execute_query()
    lib.items.add(Title="Project Alpha", Budget=50000).execute_query()
    lib.items.add(Title="Project Beta", Budget=120000).execute_query()
    lib.items.add(Title="Project Gamma", Budget=80000).execute_query()
    print(f"List: '{lib.display_name}' (3 sample items)\n")

    # -- Step 2: select only the fields you need --
    print("All items (selected fields):")
    items = lib.items.select(["id", "name"]).get().execute_query()
    for item in items:
        print(f"  {item.name} (id={item.id})")

    # -- Step 3: filter on a field value --
    print("\nBudget > 75000:")
    items = (
        lib.items.filter("fields/Budget gt 75000")
        .expand(["fields"])
        .select(["id", "name", "fields/Budget"])
        .get()
        .execute_query()
    )
    for item in items:
        print(f"  {item.name}: ${item.fields.get_property('Budget'):,}")

    # -- Step 4: top N with order --
    print("\nTop 2 items by name:")
    items = lib.items.top(2).order_by("name").select(["name"]).get().execute_query()
    for item in items:
        print(f"  {item.name}")

    if not args.keep:
        lib.delete_object().execute_query()
        print("\nList removed.")


if __name__ == "__main__":
    main()
