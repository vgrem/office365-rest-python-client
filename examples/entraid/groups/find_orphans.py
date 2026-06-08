"""
Find groups without owners or members — orphaned Microsoft 365 and
security groups.

Groups without owners are administratively unmanageable (no one can
approve membership changes). Groups without members waste directory
space and cause confusion.

Inspired by Find-GroupsNoOwnersOrMembers.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Group.Read.All       Read group membership and ownership
    User.Read.All        Read user display names
    Group.ReadWrite.All  (optional) to clean up orphaned groups

https://learn.microsoft.com/en-us/graph/api/resources/group
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def find_orphan_groups() -> tuple[list[dict], list[dict]]:
    """Find groups without owners and groups without members.

    Returns:
        Tuple of (no_owners, no_members) — lists of group dicts.
    """
    client = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    no_owners = []
    no_members = []

    groups = client.groups.get_all().execute_query()

    for group in groups:
        gid = group.id
        display = getattr(group, "display_name", "Unnamed")
        mail = getattr(group, "mail_enabled", False)
        security = getattr(group, "security_enabled", False)
        gtype = "M365" if getattr(group, "group_types", []) else "Security"

        try:
            owners = client.groups[gid].owners.get().execute_query()
            if len(owners) == 0:
                no_owners.append({
                    "id": gid,
                    "name": display,
                    "type": gtype,
                    "mail_enabled": mail,
                    "security_enabled": security,
                })
        except Exception:
            no_owners.append({
                "id": gid,
                "name": display,
                "type": gtype,
                "mail_enabled": mail,
                "security_enabled": security,
                "error": "Could not fetch owners",
            })

        try:
            members = client.groups[gid].members.get().execute_query()
            if len(members) == 0:
                no_members.append({
                    "id": gid,
                    "name": display,
                    "type": gtype,
                    "mail_enabled": mail,
                    "security_enabled": security,
                })
        except Exception:
            pass

    return no_owners, no_members


def main():
    print("Finding orphaned groups...\n")
    no_owners, no_members = find_orphan_groups()

    if no_owners:
        print(f"Groups without owners ({len(no_owners)}):\n")
        for g in no_owners:
            print(f"  {g['name']:40s}  ({g['type']})")
    else:
        print("All groups have owners. ✓\n")

    if no_members:
        print(f"Groups without members ({len(no_members)}):\n")
        for g in no_members:
            print(f"  {g['name']:40s}  ({g['type']})")
    else:
        print("All groups have at least one member. ✓")


if __name__ == "__main__":
    main()
