"""
Create a Microsoft 365 group together with its Teams team.

Team provisioning is asynchronous, so the query is retried until it completes.

Requires application permission ``Group.ReadWrite.All`` and ``Team.Create``.

https://learn.microsoft.com/en-us/graph/teams-create-group-and-team
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a group and its team")
    parser.add_argument("--keep", action="store_true", help="keep the group after creation")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.create_with_team(create_unique_name("Flight")).execute_query_retry(max_retry=10)
    print(f"Team created: {group.team.web_url}")

    if not args.keep:
        group.delete_object(permanent_delete=True).execute_query()
        print("Removed.")


if __name__ == "__main__":
    main()
