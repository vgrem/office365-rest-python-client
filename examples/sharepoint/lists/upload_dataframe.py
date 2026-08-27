"""Move data between a pandas DataFrame and a SharePoint list, both directions.

Loads a CSV (default: California housing, ~20k rows), creates the list with
typed columns if missing (fields inferred from the DataFrame dtypes), imports
all rows via the deferred ``List.from_dataframe``, then reads the list back
into a DataFrame with ``to_dataframe``.

Requires: pip install office365-rest-python-client[pandas]
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

DEFAULT_URL = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"


def main():
    import pandas as pd  # type: ignore[import-not-found]

    p = argparse.ArgumentParser(description="Import a DataFrame into a SharePoint list")
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--file")
    p.add_argument("--list-title", default="California_Housing")
    p.add_argument("--limit", type=int, default=1000, help="0 = all rows")
    args = p.parse_args()

    df = pd.read_csv(args.file or args.url)
    if args.limit > 0:
        df = df.head(args.limit)

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # Creates the list (if missing), provisions columns from the DataFrame
    # dtypes, and imports every row — all in one deferred chain.
    lst = ctx.web.lists.ensure_list(args.list_title).execute_query()
    lst.from_dataframe(df).execute_query()
    print(f"Imported {len(df)} rows into '{lst.title}'")

    # -- Export the list back into a DataFrame: .to_dataframe().execute_query().value --
    result = lst.items.get_all().select(["Id", "Title"]).to_dataframe().execute_query()
    print(f"Read back {len(result.value)} items:")
    print(result.value.head())


if __name__ == "__main__":
    main()
