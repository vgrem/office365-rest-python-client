"""
Column management — add, list, update, and delete columns.

Shows the main column types (text, number, hyperlink, lookup) including a
lookup column that references another list, then updates and removes one.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/columndefinition-create
https://learn.microsoft.com/en-us/graph/api/columndefinition-update
https://learn.microsoft.com/en-us/graph/api/columndefinition-delete
"""

import argparse

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add, list, update and delete list columns")
    parser.add_argument("--keep", action="store_true", help="keep the lists after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create a source list (lookup target) and a target list --
    categories = site.lists.add(create_unique_name("Categories"), ListTemplateType.genericList).execute_query()
    categories.items.add(Title="Finance").execute_query()
    categories.items.add(Title="Operations").execute_query()

    lib = site.lists.add(create_unique_name("Expenses"), ListTemplateType.genericList).execute_query()
    print(f"Lists: '{categories.display_name}' (lookup source), '{lib.display_name}'")

    # -- Step 2: add columns --
    lib.columns.add_text("Description", max_length=255).execute_query()
    lib.columns.add_number("Amount", minimum=0).execute_query()
    lib.columns.add_lookup("Category", categories, "Title").execute_query()
    print("  ✓ Added columns: Description (text), Amount (number), Category (lookup)")

    # -- Step 3: list columns --
    columns = lib.columns.get().execute_query()
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        print(f"  {col.name:15s}  {col.display_name}")

    # -- Step 4: update a column (rename the display name) --
    desc = next(c for c in columns if c.name == "Description")
    desc.set_property("displayName", "Details").update().execute_query()
    print("\n  ✓ Renamed 'Description' column to 'Details'")

    # -- Step 5: delete a column --
    amount = next(c for c in columns if c.name == "Amount")
    amount.delete_object().execute_query()
    print("  ✓ Deleted 'Amount' column")

    if not args.keep:
        lib.delete_object().execute_query()
        categories.delete_object().execute_query()
        print("\nLists removed.")


if __name__ == "__main__":
    main()
