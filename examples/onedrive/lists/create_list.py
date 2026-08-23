"""
Create a SharePoint list with custom columns.

Provisions a custom list, adds text/number/hyperlink columns, and looks it up
again by name. The basis for most list automation.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/list-create
https://learn.microsoft.com/en-us/graph/api/columndefinition-create
"""

import argparse

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a SharePoint list with custom columns")
    parser.add_argument("--keep", action="store_true", help="keep the list after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create the list --
    list_name = create_unique_name("Assets")
    lib = site.lists.add(list_name, ListTemplateType.genericList).execute_query()
    print(f"List created: '{lib.display_name}'")

    # -- Step 2: add columns --
    lib.columns.add_text("Category").execute_query()
    lib.columns.add_number("Amount", minimum=0).execute_query()
    lib.columns.add_hyperlink_or_picture("Documentation").execute_query()
    print("  Added columns: Category (text), Amount (number), Documentation (hyperlink)")

    # -- Step 3: list the columns --
    columns = lib.columns.get().execute_query()
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        print(f"  {col.name}  ({col.display_name})")

    # -- Step 4: find the list by name --
    found = site.lists.get_by_name(list_name).get().execute_query()
    print(f"\nFound by name: '{found.display_name}'")

    if not args.keep:
        lib.delete_object().execute_query()
        print("\nList removed.")


if __name__ == "__main__":
    main()
