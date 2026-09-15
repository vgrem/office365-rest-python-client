"""Import a pandas DataFrame into a SharePoint list (deferred, one call).

Loads a CSV (default: S&P 500 daily prices, ~1.5M rows), creates the list with
typed columns if missing (fields inferred from the DataFrame dtypes), and imports
rows via ``List.from_dataframe`` — a deferred streaming driver. Fields are
provisioned once, chunks are executed and discarded (bounded memory), and the
progress hook fires per chunk.

``--limit 40000`` (default) imports a 40k slice; ``--limit 0`` imports all.
For a memory-bounded CSV stream with concurrent batches see
``import_dataframe_large.py``.

Requires: pip install office365-rest-python-client[pandas]
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

DEFAULT_URL = "https://raw.githubusercontent.com/plotly/datasets/master/all_stocks_5yr.csv"


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p):
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)
        if p.total is not None and p.done >= p.total:
            bar.close()

    return hook


def main():
    import pandas as pd  # type: ignore[import-not-found]

    p = argparse.ArgumentParser(description="Import a DataFrame into a SharePoint list")
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--file")
    p.add_argument("--list-title", default="Stocks_5yr")
    p.add_argument("--limit", type=int, default=40000, help="rows to import (0 = all)")
    p.add_argument("--chunk", type=int, default=2000, help="rows per chunk")
    args = p.parse_args()

    df = pd.read_csv(args.file or args.url, nrows=args.limit if args.limit > 0 else None)

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # Creates the list (if missing), provisions the columns once, and imports
    # every chunk — all in one deferred chain.
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()
    stats = lst.from_dataframe(df, chunksize=args.chunk, progress=progress_bar("Importing")).execute_query().value
    print(f"\n{stats.summary()} into '{lst.title}'")


if __name__ == "__main__":
    main()
