"""
Export groups to CSV — group inventory for migration planning and audit.

Exports group identity properties. Group type (Microsoft 365 / Security /
Distribution) is derived from ``mailEnabled``/``securityEnabled`` — compute it
in your spreadsheet. Member/owner UPN lists require a query per group and are
out of scope for the ``to_csv`` pipeline.

Requires delegated permission ``Group.Read.All``, ``Directory.Read.All``.

https://learn.microsoft.com/en-us/graph/api/group-list
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

COLUMNS = ["id", "displayName", "mail", "visibility", "description", "createdDateTime", "mailEnabled", "securityEnabled"]


def main():
    parser = argparse.ArgumentParser(description="Export groups to CSV")
    parser.add_argument("--output", default="/tmp/groups_export.csv", help="output CSV file")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # Deferred: load all groups, then write the CSV after execute_query().
    with open(args.output, "w", newline="") as f:
        groups = client.groups.get_all().select(COLUMNS).to_csv(f).execute_query()

    print(f"✓ Exported {len(groups)} groups to {args.output}")


if __name__ == "__main__":
    main()
