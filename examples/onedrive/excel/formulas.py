"""
Workbook functions — evaluate Excel formulas from your code.

The functions API evaluates standard Excel functions server-side, so you can
compute results without opening Excel. Great for quick calculations in
automation pipelines.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/resources/functions
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

SAMPLE_WORKBOOK = Path(__file__).resolve().parents[2] / "data" / "Financial Sample.xlsx"


def main():
    parser = argparse.ArgumentParser(description="Evaluate Excel functions via the workbook API")
    parser.add_argument("--keep", action="store_true", help="keep the workbook after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    uploaded = client.me.drive.root.upload_file(str(SAMPLE_WORKBOOK)).execute_query()
    functions = uploaded.workbook.functions

    # -- Evaluate a few functions server-side --
    results = {
        "ABS(-2)": functions.abs(-2).execute_query().value,
        "POWER(2, 3)": functions.power(2, 3).execute_query().value,
        "DAYS(today, +10d)": functions.days(datetime.now(), datetime.now() + timedelta(days=10)).execute_query().value,
    }
    print("Function results:")
    for expression, value in results.items():
        print(f"  {expression} = {value}")

    if not args.keep:
        uploaded.delete_object().execute_query()
        print("\nWorkbook removed.")


if __name__ == "__main__":
    main()
