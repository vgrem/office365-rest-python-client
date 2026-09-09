"""Export directory users into a pandas DataFrame.

Shows the generic collection ``to_dataframe()`` on a Graph collection: page
through ``/users`` and project selected properties into a DataFrame (same
projection as ``to_csv`` / ``to_records``).

Requires application permission ``User.Read.All`` and the optional dependency
(``pip install office365-rest-python-client[pandas]``).

https://learn.microsoft.com/en-us/graph/api/user-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    p = argparse.ArgumentParser(description="Export directory users into a pandas DataFrame")
    p.add_argument(
        "--select",
        default="id,displayName,userPrincipalName,mail,jobTitle,department,country",
        help="comma-separated user properties to export",
    )
    p.add_argument("--output", default=None, help="optional CSV path to save the DataFrame")
    args = p.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("User.Read.All")
    )

    df = client.users.get_all().select(args.select.split(",")).to_dataframe().execute_query().value

    print(f"Exported {len(df):,} users x {len(df.columns)} columns\n")
    print(df.head(10).to_string(index=False))

    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
