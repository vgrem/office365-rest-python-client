"""Read a large list with a tqdm progress bar.

``get_all(progress=...)`` fires the hook once per page with a ``Progress``
snapshot (``done`` = items loaded so far). For server-driven paging the total is
unknown, so the bar is indeterminate. The coarser, print-based ``page_loaded``
callback (which receives the loaded collection) remains available too — both can
be passed at once.
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


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
    parser = argparse.ArgumentParser(description="Read a large list with a progress bar")
    parser.add_argument("--list-title", default="Contacts_Large")
    parser.add_argument("--select", default="Title,FullName,WorkCountry")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    hook = None if args.no_progress else progress_bar(f"Reading {args.list_title}")
    items = (
        ctx.web.lists.get_by_title(args.list_title)
        .items.get_all(progress=hook)
        .select(args.select.split(","))
        .execute_query()
    )
    print(f"\nRead {len(items)} items from '{args.list_title}'")


if __name__ == "__main__":
    main()
