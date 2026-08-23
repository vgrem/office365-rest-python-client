"""
Add and remove group members.

Demonstrates how to create a security group, add a user to it as a member,
and remove them again.

https://learn.microsoft.com/en-us/graph/api/group-post-members

Requires delegated permission ``Group.ReadWrite.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add and remove a group member")
    parser.add_argument("--user", required=True, help="user UPN to add as member")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    group = client.groups.create_security(
        create_unique_name("SecurityGroup"),
        description="Demo group for member management",
    ).execute_query()
    user = client.users.get_by_principal_name(args.user)

    group.members.add(user).execute_query()
    print(f"User added to group '{group.display_name}'")

    group.members.remove(user).execute_query()
    print(f"User removed from group '{group.display_name}'")

    group.delete_object(True).execute_query()
    print("Group cleaned up.")


if __name__ == "__main__":
    main()
