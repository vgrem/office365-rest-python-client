"""
Workbook tables — list, create, add rows/columns, count, and sort.

Tables give Excel data named structure (headers, banded rows, auto filters).
This example explores the existing table in the sample workbook and creates a
new one with rows and a sort applied.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/workbook-table-add
https://learn.microsoft.com/en-us/graph/api/workbook-tablerow-add
https://learn.microsoft.com/en-us/graph/api/table-sort-apply
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from office365.onedrive.workbooks.sort_field import WorkbookSortField
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="Explore and create workbook tables")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    uploaded = client.me.drive.root.upload_file(str(SAMPLE_WORKBOOK)).execute_query()
    workbook = uploaded.workbook

    # -- Step 1: list existing tables --
    tables = workbook.tables.get().execute_query()
    print(f"Existing tables ({len(tables)}):")
    for t in tables:
        print(f"  {t.name}")

    # -- Step 2: count rows and columns of the sample table --
    financials = workbook.worksheets["Sheet1"].tables["financials"].get().execute_query()
    row_count = financials.rows.count().execute_query().value
    column_count = financials.columns.count().execute_query().value
    print(f"\n'financials' table: {row_count} rows, {column_count} columns")

    # -- Step 3: read the header row and first data row --
    rows = financials.rows.get().execute_query()
    if len(rows) > 0:
        print(f"  Row 0: {rows[0].values}")

    # -- Step 4: create a new table and add a row --
    table = workbook.tables.add("A20000:C20001", True).execute_query()
    print(f"\n  Created table '{table.name}' at A20000:C20001")
    table.rows.add([["Apple", "Banana", "Cherry"]]).execute_query()
    print("  ✓ Added a data row")

    # -- Step 5: sort the new table --
    table.sort.apply([WorkbookSortField()]).execute_query()
    print("  ✓ Sorted the table")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
