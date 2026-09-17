"""Stream a large CSV into a SharePoint list — memory-bounded, resumable, idempotent.

The chunk iterator goes to ``List.import_dataframe``: the typed columns are
provisioned once, each chunk is flushed through server-side OData batches
(``--concurrency`` parallel, per-sub-request retries honoring ``Retry-After``),
and queued items are discarded after every chunk — so memory stays flat no matter
the file size.

**Idempotent** — ``key=["Name", "date"]`` hashes the natural key into a
``MigrationKey`` column, so a re-run updates/skips existing rows instead of
duplicating them. **Resumable** — the committed cursor is checkpointed after each
chunk, so an interrupted run continues where it stopped.

    python import_dataframe_large.py --rows 40000 --concurrency 5

Requires: pip install office365-rest-python-client[pandas]
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

CSV_URL = "https://raw.githubusercontent.com/plotly/datasets/master/all_stocks_5yr.csv"


def main():
    import pandas as pd  # type: ignore[import-not-found]

    p = argparse.ArgumentParser(description="Stream a large CSV into a SharePoint list")
    p.add_argument("--list-title", default="Stocks_5yr_Large")
    p.add_argument("--rows", type=int, default=40000, help="rows to import (0 = all)")
    p.add_argument("--chunk", type=int, default=2000, help="rows per memory slice")
    p.add_argument("--concurrency", type=int, default=5, help="parallel batch requests")
    p.add_argument("--checkpoint", default="stocks.checkpoint.json", help="'' disables resume")
    p.add_argument("--progress", action="store_true", help="show a live tqdm progress bar")
    args = p.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()
    chunks = pd.read_csv(CSV_URL, chunksize=args.chunk, nrows=args.rows or None)

    bar = None
    progress = None
    if args.progress:
        from tqdm import tqdm

        resumed = 0
        if args.checkpoint:
            from office365.runtime.imports import FileCheckpointStore

            resumed = FileCheckpointStore(args.checkpoint).load().cursor
        bar = tqdm(
            total=args.rows or None,
            initial=resumed,
            unit="row",
            unit_scale=True,
            desc="Importing",
            dynamic_ncols=True,
        )
        progress = lambda p: bar.update(p.done - bar.n)  # noqa: E731

    driver = lst.import_dataframe(
        chunks,
        checkpoint=args.checkpoint or None,
        key=["Name", "date"],
        progress=progress,
        total=args.rows or None,
    )
    if driver.resumed_from:
        print(f"Resuming from {driver.resumed_from:,} committed row(s)")

    try:
        stats = driver.execute_batch(concurrency=args.concurrency).value
    except KeyboardInterrupt:
        if bar is not None:
            bar.close()
        print(f"Interrupted at {driver.checkpoint.cursor:,} row(s) — re-run to resume")
        raise SystemExit(130) from None
    if bar is not None:
        bar.close()

    print(f"{stats.summary()} into '{lst.title}'")


if __name__ == "__main__":
    main()
