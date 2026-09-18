"""Write a pandas DataFrame to a SharePoint document library as CSV or XLSX.

``Folder.write_dataframe`` serializes the frame and writes it as a file. CSV is
written UTF-8 with a BOM (``utf-8-sig``) so Excel opens it with the columns
intact; pass ``--format xlsx`` for a worksheet (requires the ``[excel]`` extra).
The symmetric read is ``Folder.read_dataframe`` / ``File.read_dataframe``.

Requires: pip install office365-rest-python-client[pandas]
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    import pandas as pd  # type: ignore[import-not-found]

    parser = argparse.ArgumentParser(description="Upload a DataFrame to a SharePoint library")
    parser.add_argument("--list-title", default="Documents", help="document library title")
    parser.add_argument("--name", default="stocks.csv", help="file name to create")
    parser.add_argument("--format", default="csv", choices=["csv", "xlsx"], help="file format")
    parser.add_argument("--path", default=None, help="source CSV path (default: a small sample)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = ctx.web.lists.get_by_title(args.list_title).root_folder

    df = pd.read_csv(args.path) if args.path else pd.DataFrame({"Name": ["AAPL", "MSFT"], "Close": [120.5, 230.1]})
    file = folder.write_dataframe(args.name, df, format=args.format).execute_query()
    print(f"Uploaded {len(df)} row(s) to {file.server_relative_url}")


if __name__ == "__main__":
    main()
