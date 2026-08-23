"""
Create a Microsoft 365 group with an associated team.

https://learn.microsoft.com/en-us/graph/teams-create-group-and-team

Requires delegated permission ``Group.ReadWrite.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def print_failure(retry_number, _ex):
    print(f"{retry_number}: Team creation still in progress, waiting...")


def main():
    parser = argparse.ArgumentParser(description="Create a group and its team")
    parser.add_argument("--name", default=create_unique_name("Flight"), help="group display name")
    parser.add_argument("--keep", action="store_true", help="keep the group after creation")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.create_with_team(args.name).execute_query_retry(max_retry=10, failure_callback=print_failure)
    print(f"Team has been created:  {group.team.web_url}")

    if not args.keep:
        group.delete_object(True).execute_query()
        print("Group cleaned up.")


if __name__ == "__main__":
    main()
