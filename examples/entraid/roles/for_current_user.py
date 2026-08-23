"""
List the directory roles for the current (signed-in) user.

Uses a delegated user context (``me`` is not available to app-only clients).

https://learn.microsoft.com/en-us/graph/api/user-list-memberof?view=graph-rest-1.0

Requires delegated permission ``RoleManagement.Read.Directory``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    me = client.me.get().execute_query()
    print(f"Directory roles for {me}:")

    roles = client.me.get_directory_roles().execute_query()
    for role in roles:
        print(f"User has role: {role}")


if __name__ == "__main__":
    main()
