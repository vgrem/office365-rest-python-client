"""
List the members of an Entra ID directory role.

Directory role members are polymorphic ``directoryObject`` entries: each member
is mapped to its concrete type (``User``, ``Group``, ``Device``, ...) based on
the ``@odata.type`` reported by Graph.

Requires delegated permission ``RoleManagement.Read.Directory``
(or ``Directory.Read.All``).

    python list_role_members.py
    python list_role_members.py --role "Security Administrator"

https://learn.microsoft.com/en-us/graph/api/directoryrole-list-members
"""

import argparse

from office365.directory.groups.group import Group
from office365.directory.users.user import User
from office365.graph_client import GraphClient
from office365.intune.devices.device import Device
from tests.settings import client_id, client_secret, tenant


def _describe(member) -> str:
    if isinstance(member, User):
        return f"User: {member.get_property('userPrincipalName') or member.get_property('id')}"
    if isinstance(member, Group):
        return f"Group: {member.get_property('displayName') or member.get_property('id')}"
    if isinstance(member, Device):
        return f"Device: {member.get_property('displayName') or member.get_property('id')}"
    return f"{member.entity_type_name}: {member.get_property('displayName') or member.get_property('id')}"


def main():
    parser = argparse.ArgumentParser(description="List members of a directory role")
    parser.add_argument(
        "--role",
        default="Global Administrator",
        help="role display name, e.g. 'Security Administrator' (default: 'Global Administrator')",
    )
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    role = client.directory_roles.get_by_name(args.role).get().execute_query()
    members = role.members.get().execute_query()
    print(f"Members of '{role.get_property('displayName')}' ({len(members)}):")
    for member in members:
        print(f"  {_describe(member)}")


if __name__ == "__main__":
    main()
