"""
Assign a manager to a user (org hierarchy).

    python assign_manager.py --user user@contoso.onmicrosoft.com --manager boss@contoso.onmicrosoft.com

https://learn.microsoft.com/en-us/graph/api/user-post-manager?view=graph-rest-1.0

Requires delegated permission ``User.ReadWrite.All`` (reading the manager back
needs ``User.Read.All`` or an equivalent).
"""

import argparse

from office365.graph_client import GraphClient
from tests import test_user_principal_name, test_user_principal_name_alt
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Assign a manager to a user")
    parser.add_argument("--user", default=test_user_principal_name, help="the employee's user principal name")
    parser.add_argument("--manager", default=test_user_principal_name_alt, help="the manager's user principal name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    user = client.users.get_by_principal_name(args.user).get().execute_query()
    manager = client.users.get_by_principal_name(args.manager).get().execute_query()
    assert user.id is not None

    user.assign_manager(manager).execute_query()

    assigned_ref = user.manager.get().execute_query()
    assert assigned_ref.id is not None
    assigned = client.users[assigned_ref.id].get().execute_query()
    print(f"Assigned manager for {user.user_principal_name}: {assigned.display_name} ({assigned.user_principal_name})")


if __name__ == "__main__":
    main()
