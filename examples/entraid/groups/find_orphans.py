"""
Find groups without owners or members — orphaned Microsoft 365 and
security groups.

Groups without owners are administratively unmanageable (no one can
approve membership changes). Groups without members waste directory
space and cause confusion.

Required delegated permissions:
    Group.Read.All       Read group membership and ownership
    User.Read.All        Read user display names
    Group.ReadWrite.All  (optional) to clean up orphaned groups

https://learn.microsoft.com/en-us/graph/api/resources/group
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def find_orphan_groups() -> tuple[list, list]:
    """Find groups without owners and groups without members.

    Returns:
        Tuple of (no_owners, no_members) — lists of Group objects.
    """
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    no_owners = []
    no_members = []

    groups = client.groups.get_all().execute_query()

    for group in groups:
        try:
            if not group.owners.get().execute_query():
                no_owners.append(group)
        except Exception:
            no_owners.append(group)

        try:
            if not group.members.get().execute_query():
                no_members.append(group)
        except Exception:
            pass

    return no_owners, no_members


def main():
    print("Finding orphaned groups...\n")
    no_owners, no_members = find_orphan_groups()

    if no_owners:
        print(f"Groups without owners ({len(no_owners)}):\n")
        for g in no_owners:
            t = "M365" if g.group_types else "Security"
            print(f"  {(g.display_name or 'Unnamed'):40s}  ({t})")
    else:
        print("All groups have owners. ✓\n")

    if no_members:
        print(f"Groups without members ({len(no_members)}):\n")
        for g in no_members:
            t = "M365" if g.group_types else "Security"
            print(f"  {(g.display_name or 'Unnamed'):40s}  ({t})")
    else:
        print("All groups have at least one member. ✓")


if __name__ == "__main__":
    main()
