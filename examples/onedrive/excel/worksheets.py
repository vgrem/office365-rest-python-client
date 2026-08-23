"""
Worksheets — list, add, read, protect, and delete.

Each workbook is organized into worksheets. This example walks through the
common worksheet lifecycle: enumerate, add, read the used range, protect
against edits, and remove.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/worksheet-list
https://learn.microsoft.com/en-us/graph/api/worksheet-protection
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from office365.onedrive.workbooks.worksheets.protection_options import WorkbookWorksheetProtectionOptions
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="List, add, read, protect and delete worksheets")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    uploaded = client.me.drive.root.upload_file(str(SAMPLE_WORKBOOK)).execute_query()
    workbook = uploaded.workbook

    # -- Step 1: list worksheets --
    worksheets = workbook.worksheets.get().execute_query()
    print(f"Worksheets ({len(worksheets)}):")
    for ws in worksheets:
        print(f"  {ws.name}")

    # -- Step 2: read the used range of the first sheet --
    first_name = worksheets[0].name
    if first_name:
        sheet = workbook.worksheets[first_name].get().execute_query()
        used = sheet.used_range(values_only=True).execute_query()
        print(f"\nUsed range of '{sheet.name}': {used.address}")
        if used.values:
            for row in used.values[:5]:
                print(f"  {row}")

    # -- Step 3: add a worksheet --
    new_sheet = workbook.worksheets.add(create_unique_name("Sheet")).execute_query()
    print(f"\n  Added worksheet '{new_sheet.name}'")

    # -- Step 4: protect it --
    new_sheet.protection.protect(WorkbookWorksheetProtectionOptions(allowDeleteRows=False)).execute_query()
    print("  ✓ Worksheet protected (deleting rows disallowed)")

    # -- Step 5: delete the worksheet --
    new_sheet.delete_object().execute_query()
    print("  ✓ Worksheet deleted")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
