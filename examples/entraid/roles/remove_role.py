"""
Remove a user from an Entra ID directory role (e.g., Security Administrator).

Requires a privileged admin account with Global Administrator or
Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/api/directoryrole-delete-member
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Remove a user from a directory role")
    parser.add_argument("--role", required=True, help="role display name, e.g. 'Security Administrator'")
    parser.add_argument("--user", required=True, help="user UPN, e.g. user@contoso.com")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    role = client.directory_roles.get_by_name(args.role).get().execute_query()
    role.remove_member(args.user).execute_query()
    print(f"✓ Removed {args.user} from role '{role.display_name}'")


if __name__ == "__main__":
    main()
