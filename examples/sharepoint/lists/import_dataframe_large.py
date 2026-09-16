"""Stream a large CSV into a SharePoint list with concurrent batches.

Reads the CSV **in memory-bounded chunks** (``pd.read_csv(..., chunksize=)``) and
hands the chunk iterator to ``List.import_dataframe``. The driver provisions the
typed columns once from the first chunk, then queues and flushes each chunk
through server-side OData batches — ``concurrency`` runs those batches in
parallel, each throttled sub-request retried honoring ``Retry-After``. Queued
items are discarded after every chunk, so memory stays flat regardless of file
size.

For long-running jobs, ``--checkpoint`` persists the committed cursor after each
chunk: re-run the same command to resume where it stopped. ``--on-error collect``
records and skips a failing chunk instead of aborting.

The import is **idempotent**: ``--key Name,date`` stores a hash of those columns
in a ``MigrationKey`` field and, on re-run, existing rows are updated
(``--on-conflict upsert``, default) or skipped (``--on-conflict skip``) instead
of duplicated — no checkpoint required.

Default source: S&P 500 daily prices (~1.5M rows). ``--rows 40000`` (default)
shows the fast path on a 40k slice; ``--rows 0`` imports the whole file.

    python import_dataframe_large.py --rows 40000 --concurrency 5 --checkpoint run.json

Requires: pip install office365-rest-python-client[pandas]
"""

from __future__ import annotations

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

DEFAULT_URL = "https://raw.githubusercontent.com/plotly/datasets/master/all_stocks_5yr.csv"


def progress_bar(no_progress: bool):
    """Optional tqdm hook counting imported rows (indeterminate for a CSV stream)."""
    if no_progress:
        return None
    from tqdm import tqdm

    bar = tqdm()
    state = {"n": 0}

    def hook(p):
        bar.update(p.done - state["n"])
        state["n"] = p.done

    return hook


def committed_rows(checkpoint_path: str | None) -> int:
    """Rows already committed in the checkpoint (0 when absent/disabled)."""
    if not checkpoint_path:
        return 0
    from pathlib import Path

    from office365.runtime.imports import ImportCheckpoint

    path = Path(checkpoint_path)
    return ImportCheckpoint.load(path).cursor if path.exists() else 0


def main():
    import pandas as pd  # type: ignore[import-not-found]

    p = argparse.ArgumentParser(description="Stream a large CSV into a SharePoint list")
    p.add_argument("--url", default=DEFAULT_URL, help="CSV URL")
    p.add_argument("--file", default=None, help="local CSV path (overrides --url)")
    p.add_argument("--list-title", default="Stocks_5yr_Large")
    p.add_argument("--rows", type=int, default=40000, help="rows to import (0 = all)")
    p.add_argument("--chunk", type=int, default=2000, help="rows per memory slice")
    p.add_argument("--items-per-batch", type=int, default=100, help="item creates per batch request")
    p.add_argument("--concurrency", type=int, default=5, help="parallel batch requests")
    p.add_argument("--checkpoint", default=None, help="checkpoint path (default: <list-title>.checkpoint.json)")
    p.add_argument("--no-checkpoint", action="store_true", help="disable checkpointing/resume")
    p.add_argument("--on-error", choices=("raise", "collect"), default="raise", help="failed-chunk policy")
    p.add_argument("--key", default="Name,date", help="natural-key column(s) for idempotency ('' disables)")
    p.add_argument("--on-conflict", choices=("skip", "upsert"), default="upsert", help="existing-key policy")
    p.add_argument("--enforce-unique", action="store_true", help="make the key column unique on the list")
    p.add_argument("--dry-run", action="store_true", help="plan only (no writes)")
    p.add_argument("--no-progress", action="store_true", help="do not show tqdm progress")
    args = p.parse_args()
    key = [c.strip() for c in args.key.split(",") if c.strip()] or None

    checkpoint = None if args.no_checkpoint else (args.checkpoint or f"{args.list_title}.checkpoint.json")
    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()

    done_before = committed_rows(checkpoint)
    if done_before:
        print(f"Resuming: {done_before:,} row(s) already committed — skipping them")

    # Re-read the same source; the driver skips the committed chunks on resume.
    chunks = pd.read_csv(
        args.file or args.url,
        chunksize=args.chunk,
        nrows=args.rows if args.rows > 0 else None,
    )
    try:
        stats = (
            lst.import_dataframe(
                chunks,
                progress=progress_bar(args.no_progress),
                checkpoint=checkpoint,
                on_error=args.on_error,
                key=key,
                on_conflict=args.on_conflict,
                enforce_unique=args.enforce_unique,
                dry_run=args.dry_run,
            )
            .execute_batch(items_per_batch=args.items_per_batch, concurrency=args.concurrency)
            .value
        )
    except KeyboardInterrupt:
        print(f"\nInterrupted after {committed_rows(checkpoint):,} row(s). Re-run the same command to resume.")
        raise SystemExit(130) from None
    except Exception as ex:  # noqa: BLE001 — report and point at the resumable checkpoint
        print(f"\nImport failed: {ex}")
        print(f"Committed {committed_rows(checkpoint):,} row(s). Re-run the same command to resume.")
        raise SystemExit(1) from ex

    print(f"\n{stats.summary()} into '{lst.title}'")
    if checkpoint:
        print(f"Checkpoint: {checkpoint} ({committed_rows(checkpoint):,} rows committed)")


if __name__ == "__main__":
    main()
