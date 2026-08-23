"""
Assign an Entra ID directory role (e.g., Security Administrator) to a user.

If the role hasn't been activated in the tenant yet, it will be activated first.

Requires a privileged admin account with Global Administrator or
Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/api/directoryrole-post-members
"""

import argparse
import sys

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import DuplicatedObjectException
from office365.runtime.types.exceptions import NotFoundException
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Assign a directory role to a user")
    parser.add_argument("--role", required=True, help="role display name, e.g. 'Security Administrator'")
    parser.add_argument("--user", required=True, help="user UPN, e.g. user@contoso.com")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # Activate the role (idempotent — DuplicatedObjectException means already active)
    try:
        client.directory_roles.assign(args.role).execute_query()
    except DuplicatedObjectException:
        pass

    try:
        role = client.directory_roles.get_by_name(args.role).get().execute_query()
    except NotFoundException:
        print(f"❌ Role '{args.role}' not found after activation.")
        sys.exit(1)

    role.add_member(args.user).execute_query()
    print(f"✅ Role '{role.display_name}' assigned to {args.user}")


if __name__ == "__main__":
    main()
