"""
Add and remove group owners.

Demonstrates how to add a user to a group's owners and remove them again.

https://learn.microsoft.com/en-us/graph/api/group-post-owners
https://learn.microsoft.com/en-us/graph/api/group-delete-owners
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add and remove a group owner")
    parser.add_argument("--group", required=True, help="group display name")
    parser.add_argument("--user", required=True, help="user UPN to add as owner")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.get_by_name(args.group).get().execute_query()
    user = client.users.get_by_principal_name(args.user)

    group.owners.add(user).execute_query()
    print(f"Added {args.user} as owner of '{group.display_name}'")

    group.owners.remove(user).execute_query()
    print(f"Removed {args.user} from owners of '{group.display_name}'")


if __name__ == "__main__":
    main()
