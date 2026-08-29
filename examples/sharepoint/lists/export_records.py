"""
Export a SharePoint list to the same data in records, CSV, NDJSON, and Excel.

Demonstrates the shared record projection (``to_records``) and the format
adapters built on it (``to_csv``, ``to_ndjson``, ``to_excel``).
"""

import argparse
import io
import json
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Export a list to records / CSV / NDJSON / Excel")
    parser.add_argument("--list-title", default="Documents", help="list or library title")
    parser.add_argument("--select", default=None, help="comma-separated fields to export")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    items = ctx.web.lists.get_by_title(args.list_title).items
    select = args.select.split(",") if args.select else ["Id", "Title"]
    loaded = items.select(select).get_all().execute_query()

    # 1. Neutral records form
    records = loaded.to_records()
    print(f"to_records: {len(records)} records")
    if records:
        print(f"  first record: {records[0]}")

    # 2. CSV
    csv_file = io.StringIO()
    loaded.to_csv(csv_file).execute_query()
    print(f"to_csv: {len(csv_file.getvalue())} chars")

    # 3. NDJSON — one JSON object per line
    ndjson_file = io.StringIO()
    loaded.to_ndjson(ndjson_file).execute_query()
    first = next(iter(json.loads(line) for line in ndjson_file.getvalue().splitlines()), None)
    print(f"to_ndjson: {first}")

    # 4. Excel
    output_dir = tempfile.mkdtemp()
    xlsx_path = os.path.join(output_dir, "export.xlsx")
    loaded.to_excel(xlsx_path).execute_query()
    print(f"to_excel: wrote {os.path.getsize(xlsx_path)} bytes to {xlsx_path}")


if __name__ == "__main__":
    main()
