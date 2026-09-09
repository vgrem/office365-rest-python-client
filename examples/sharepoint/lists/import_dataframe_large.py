"""Load a large DataFrame (open dataset) into a SharePoint list fast.

Reads a remote CSV **in memory-bounded chunks** (``pd.read_csv(..., chunksize=)``),
provisions the typed columns once from the first chunk's dtypes, then feeds each
chunk through the collection-level ``from_dataframe`` and submits the queued
item creates with ``execute_batch`` (server-side batches, run in parallel with
``--concurrency``, retrying throttled sub-requests).

Default source: S&P 500 daily prices (~1.5M rows). ``--rows 40000`` (default)
shows the fast path on a 40k slice; ``--rows 0`` imports the whole file.

    python import_dataframe_large.py --rows 40000 --concurrency 5

Requires: pip install office365-rest-python-client[pandas]
https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

DEFAULT_URL = "https://raw.githubusercontent.com/plotly/datasets/master/all_stocks_5yr.csv"


def progress_bar(total: int | None, no_progress: bool):
    """Optional tqdm hook counting imported rows (indeterminate when total unknown)."""
    if no_progress:
        return None
    from tqdm import tqdm

    bar = tqdm(total=total)
    state = {"n": 0}

    def hook(done: int) -> None:
        bar.update(done - state["n"])
        state["n"] = done

    return hook


def main():
    p = argparse.ArgumentParser(description="Bulk-import an open CSV into a SharePoint list (fast)")
    p.add_argument("--url", default=DEFAULT_URL, help="CSV URL")
    p.add_argument("--file", default=None, help="local CSV path (overrides --url)")
    p.add_argument("--list-title", default="Stocks_5yr_Large")
    p.add_argument("--rows", type=int, default=40000, help="rows to import (0 = all)")
    p.add_argument("--chunk", type=int, default=2000, help="rows per memory slice")
    p.add_argument("--items-per-batch", type=int, default=100, help="item creates per batch request")
    p.add_argument("--concurrency", type=int, default=5, help="parallel batch requests")
    p.add_argument("--no-progress", action="store_true", help="do not show tqdm progress")
    args = p.parse_args()

    import pandas as pd  # type: ignore[import-not-found]

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()

    # Memory-bounded streaming read: one DataFrame slice at a time
    reader = pd.read_csv(args.file or args.url, chunksize=args.chunk)
    hook = progress_bar(args.rows if args.rows > 0 else None, args.no_progress)
    total_rows = args.rows if args.rows > 0 else None
    done = 0
    first = True

    for chunk_df in reader:
        if total_rows is not None and done >= total_rows:
            break
        slice_df = chunk_df.head(total_rows - done) if total_rows is not None else chunk_df

        if first:
            # Provision the typed columns once (not per chunk)
            lst.fields.from_dataframe(slice_df).execute_query()
            first = False

        # Reuse the collection-level adapter, then flush the queued creates in
        # server-side batches (optionally concurrent)
        lst.items.from_dataframe(slice_df)
        ctx.execute_batch(items_per_batch=args.items_per_batch, concurrency=args.concurrency)

        done += len(slice_df)
        if hook is not None:
            hook(done)

    if hook is not None:
        hook.close()  # type: ignore[attr-defined]
    print(f"Imported {done:,} rows into '{lst.title}'")


if __name__ == "__main__":
    main()
