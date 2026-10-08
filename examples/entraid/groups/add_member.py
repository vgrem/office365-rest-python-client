"""
Add and remove a group member.

Members can be users, service principals, or nested groups.

Requires application permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/group-post-members
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add and remove a group member")
    parser.add_argument("--group", required=True, help="group display name")
    parser.add_argument("--user", required=True, help="user UPN")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.find_by_name(args.group, required=True).execute_query()
    user = client.users.get_by_principal_name(args.user)

    group.members.add(user).execute_query()
    print(f"Added {args.user} to '{group.display_name}'")
    group.members.remove(user).execute_query()
    print(f"Removed {args.user} from '{group.display_name}'")


if __name__ == "__main__":
    main()
