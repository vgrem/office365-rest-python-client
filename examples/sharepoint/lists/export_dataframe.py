"""Export a SharePoint list back into a pandas DataFrame.

Reads a list (default: the California_Housing list created by
``import_dataframe.py``) and materializes it into a DataFrame via the deferred
``to_dataframe()`` — ``.execute_query().value`` holds the result.

The symmetric counterpart (importing a DataFrame into a list) is
``import_dataframe.py``.

Requires: pip install office365-rest-python-client[pandas]
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def _page_loaded(col) -> None:
    """Built-in progress demo — no tqdm needed.

    ``get_all(page_loaded=...)`` fires once per page with the loaded collection;
    print how far the read has progressed.
    """
    print(f"  loaded {len(col)} items so far")


def main():
    p = argparse.ArgumentParser(description="Export a SharePoint list into a pandas DataFrame")
    p.add_argument("--list-title", default="California_Housing")
    p.add_argument(
        "--select",
        default="Id,median_income,housing_median_age",
        help="comma-separated fields to export",
    )
    p.add_argument("--no-progress", action="store_true", help="do not print per-page progress")
    args = p.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    df = (
        ctx.web.lists.get_by_title(args.list_title)
        .items.get_all(page_loaded=None if args.no_progress else _page_loaded)
        .select(args.select.split(","))
        .to_dataframe()
        .execute_query()
        .value
    )

    print(f"Read back {len(df)} items:")
    print(df.head())


if __name__ == "__main__":
    main()
