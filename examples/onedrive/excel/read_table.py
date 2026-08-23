"""
Read Excel tables and range data using workbook sessions.

Workbook sessions allow consistent reads across a workbook. This example
uploads the sample workbook, lists its tables, and prints the table data.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/excel
https://learn.microsoft.com/en-us/graph/api/workbook-list-tables
https://learn.microsoft.com/en-us/graph/api/workbook-tablerow-list
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="Read workbook tables and their data")
    parser.add_argument("--path", help="path to an .xlsx file (default: the bundled sample workbook)")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- Step 1: upload an Excel file --
    local_path = args.path or SAMPLE_WORKBOOK
    uploaded = client.me.drive.root.upload_file(str(local_path)).execute_query()
    print(f"Uploaded: {uploaded.name}")
    workbook = uploaded.workbook

    # -- Step 2: list tables --
    tables = workbook.tables.get().execute_query()
    print(f"\nTables ({len(tables)}):")
    for t in tables:
        rows = t.rows.get().execute_query()
        print(f"  {t.name:30s}  rows: {len(rows)}")

    # -- Step 3: print the first table's data --
    if tables:
        print(f"\nData in '{tables[0].name}':")
        for row in tables[0].rows:
            print(f"  {row.values}")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
