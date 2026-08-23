"""
List the directory roles assigned to a specific user.

https://learn.microsoft.com/en-us/graph/api/user-list-memberof?view=graph-rest-1.0

Requires delegated permission ``RoleManagement.Read.Directory``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List the directory roles for a user")
    parser.add_argument("--user", required=True, help="user UPN, e.g. user@contoso.com")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    roles = client.users.get_by_principal_name(args.user).get_directory_roles().execute_query()
    for role in roles:
        print(f"User has role: {role.display_name}")


if __name__ == "__main__":
    main()
