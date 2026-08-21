"""Import a pandas DataFrame into a SharePoint list in batches.

Loads a CSV (default: California housing, ~20k rows), creates the list with
typed columns if missing, uploads rows via execute_batch.

Requires: pip install office365-rest-python-client[notebooks]
"""

import argparse
import re

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import client_id, password, team_site_url, tenant, username

DEFAULT_URL = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"


def _name(col: str) -> str:
    """SharePoint field internal names cannot contain spaces or punctuation."""
    return re.sub(r"\W", "_", col)


def _value(v):
    """Convert a numpy scalar cell to a JSON-safe native value."""
    return v.item() if hasattr(v, "item") else v


def main():
    import pandas as pd

    p = argparse.ArgumentParser(description="Upload a DataFrame to a SharePoint list")
    p.add_argument("--url", default=DEFAULT_URL)
    p.add_argument("--file")
    p.add_argument("--list-title", default="California_Housing")
    p.add_argument("--limit", type=int, default=1000, help="0 = all rows")
    p.add_argument("--batch-size", type=int, default=100)
    args = p.parse_args()

    df = pd.read_csv(args.file or args.url)
    if args.limit > 0:
        df = df.head(args.limit)

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    lst = ctx.web.lists.get_by_title(args.list_title)
    try:
        lst.get().execute_query()
    except ClientRequestException:
        lst = ctx.web.lists.add_list(args.list_title, "", ListTemplateType.GenericList)
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                lst.fields.add_number(_name(col))
            else:
                lst.fields.add_text_field(_name(col))
        ctx.execute_query()

    for _, row in df.iterrows():
        lst.add_item({_name(c): _value(row[c]) for c in df.columns if not pd.isna(row[c])})
    ctx.execute_batch(items_per_batch=args.batch_size)


if __name__ == "__main__":
    main()
