"""
List group members.

Lists all direct members of a group — includes users, service principals,
and nested groups.

https://learn.microsoft.com/en-us/graph/api/group-list-members

Requires delegated permission ``Group.Read.All`` or ``Group.ReadWrite.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List a group's members")
    parser.add_argument("--group", required=True, help="group display name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.get_by_name(args.group).get().execute_query()

    members = group.members.get().execute_query()
    print(f"Members of '{group.display_name}' ({len(members)}):")
    for m in members:
        rtype = m.get_property("resourceType") or "?"
        name = m.get_property("displayName") or "?"
        print(f"  {rtype:<20s}  {name:40s}  {m.id}")


if __name__ == "__main__":
    main()
