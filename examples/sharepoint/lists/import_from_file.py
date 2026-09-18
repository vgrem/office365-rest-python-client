"""Import a CSV/XLSX stored in a SharePoint library into a list.

``List.import_from_file`` downloads the file from the current site (honoring auth)
and streams it into the list — bounded memory, resumable, and idempotent with
``--key`` (a ``MigrationKey`` column is created and each row is skipped/upserted).

    python import_from_file.py --file-url "Shared Documents/stocks.csv" --key Name date

Requires: pip install office365-rest-python-client[pandas]
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Import a SharePoint-hosted file into a list")
    parser.add_argument("--list-title", default="Stocks_5yr_Large")
    parser.add_argument("--file-url", default="Shared Documents/stocks.csv", help="server-relative file URL")
    parser.add_argument("--format", default="csv", choices=["csv", "xlsx"], help="file format")
    parser.add_argument("--chunk", type=int, default=2000, help="rows per memory slice")
    parser.add_argument("--concurrency", type=int, default=5, help="parallel batch requests")
    parser.add_argument("--key", nargs="*", default=["Name", "date"], help="natural key column(s)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()

    driver = lst.import_from_file(
        args.file_url,
        format=args.format,
        chunksize=args.chunk,
        key=args.key or None,
        checkpoint="stocks.file.checkpoint.json",
    )
    stats = driver.execute_batch(concurrency=args.concurrency).value
    print(f"{stats.summary()} into '{lst.title}'")


if __name__ == "__main__":
    main()
