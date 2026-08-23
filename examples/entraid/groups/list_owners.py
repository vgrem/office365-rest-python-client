"""
List the owners of a group.

https://learn.microsoft.com/en-us/graph/api/group-list-owners
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List a group's owners")
    parser.add_argument("--group", required=True, help="group display name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.get_by_name(args.group).get().execute_query()

    owners = group.owners.get().execute_query()
    print(f"Owners of '{group.display_name}' ({len(owners)}):")
    for owner in owners:
        upn = owner.get_property("userPrincipalName") or "?"
        name = owner.get_property("displayName") or ""
        print(f"  {upn}  {name}")


if __name__ == "__main__":
    main()
