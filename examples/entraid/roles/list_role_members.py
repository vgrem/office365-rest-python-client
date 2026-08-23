"""
List the members of an Entra ID directory role.

Requires delegated permission ``RoleManagement.Read.Directory``
(or ``Directory.Read.All``).

https://learn.microsoft.com/en-us/graph/api/directoryrole-list-members
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List members of a directory role")
    parser.add_argument("--role", required=True, help="role display name, e.g. 'Security Administrator'")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    role = client.directory_roles.get_by_name(args.role).get().execute_query()
    members = role.members.get().execute_query()
    print(f"Members of '{role.display_name}' ({len(members)}):")
    for member in members:
        upn = member.get_property("userPrincipalName") or "?"
        name = member.get_property("displayName") or ""
        print(f"  {upn}  {name}")


if __name__ == "__main__":
    main()
