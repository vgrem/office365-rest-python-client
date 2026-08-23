"""
Ranges — read and write cell values, plus named items.

Ranges are how you get at cell data. This example writes values to a range,
reads them back, finds the used range, creates a named item, and cleans up.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/range-update
https://learn.microsoft.com/en-us/graph/api/range-get
https://learn.microsoft.com/en-us/graph/api/workbook-nameditem-add
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="Read and write cell ranges in a workbook")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    uploaded = client.me.drive.root.upload_file(str(SAMPLE_WORKBOOK)).execute_query()
    workbook = uploaded.workbook
    sheet = workbook.worksheets["Sheet1"].get().execute_query()

    # -- Step 1: write values to a range --
    values = [
        ["Region", "Q1", "Q2"],
        ["North", 100, 120],
        ["South", 90, 110],
    ]
    sheet.range("F20:H22").set_property("values", values).update().execute_query()
    print("  ✓ Wrote 3x3 values to F20:H22")

    # -- Step 2: read the values back --
    rng = sheet.range("F20:H22").select(["values"]).get().execute_query()
    print("  Read back:")
    if rng.values:
        for row in rng.values:
            print(f"    {row}")

    # -- Step 3: find the used range of the worksheet --
    used = sheet.used_range().execute_query()
    print(f"\n  Used range of '{sheet.name}': {used.address}")

    # -- Step 4: create a named item pointing at the range --
    named = workbook.names.add("DemoRange", "=Sheet1!$F$20:$H$22", "Demo named range").execute_query()
    print(f"  ✓ Named item '{named.name}' created")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
