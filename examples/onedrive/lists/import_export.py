"""
Bulk import and export list items (JSON in, CSV out).

Loads many records into a list from a JSON structure with a single query per
record queued together, then exports the result back to CSV — a common
migration/backup workflow for SharePoint lists.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/listitem-create
"""

import argparse
import io

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant

records = [
    {"Title": "Northwind", "Region": "North", "Revenue": 120000},
    {"Title": "Contoso", "Region": "West", "Revenue": 86000},
    {"Title": "Fabrikam", "Region": "East", "Revenue": 150000},
    {"Title": "Adventure Works", "Region": "South", "Revenue": 98000},
]


def main():
    parser = argparse.ArgumentParser(description="Bulk import list items from JSON and export to CSV")
    parser.add_argument("--keep", action="store_true", help="keep the list after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    site = client.sites.root

    # -- Step 1: create a list --
    lib = site.lists.add(create_unique_name("Revenue"), ListTemplateType.genericList).execute_query()
    lib.columns.add_number("Revenue").execute_query()
    print(f"List: '{lib.display_name}'")

    # -- Step 2: bulk import from JSON (queued in one execute) --
    lib.items.from_json(records).execute_query()
    print(f"  ✓ Imported {len(records)} items from JSON")

    # -- Step 3: export back to CSV --
    buffer = io.StringIO()
    lib.items.expand(["fields"]).select(["id", "fields/Title", "fields/Revenue"]).to_csv(buffer).execute_query()
    print("\nExported CSV:")
    print(buffer.getvalue())

    if not args.keep:
        lib.delete_object().execute_query()
        print("List removed.")


if __name__ == "__main__":
    main()
