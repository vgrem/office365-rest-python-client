"""
Directory groups: list groups with owners, members, and find
orphaned groups (no owners or no members).

Also shows dynamic group creation for Entra ID.

Requires delegated permission ``Group.Read.All``, ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/group-list
https://learn.microsoft.com/en-us/graph/api/group-post-dynamicgroup
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. List groups with membership counts
groups = client.groups.top(20).get().execute_query()
print(f"Groups ({len(groups)}):")
orphaned = []
for g in groups:
    members = g.members.get().execute_query()
    owners = g.owners.get().execute_query()
    has_owners = len(owners) > 0
    has_members = len(members) > 0
    status = "✔" if has_owners and has_members else "⚠" if not has_owners else " "
    if not has_owners or not has_members:
        orphaned.append(g)
    print(f"  {status}  {g.display_name:35s}  owners: {len(owners):2d}  members: {len(members):3d}")

if orphaned:
    print(f"\nOrphaned groups ({len(orphaned)}):")
    for g in orphaned:
        print(f"  ⚠ {g.display_name}")
