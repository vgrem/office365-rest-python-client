"""
Delete a single group by name.

The simplest delete flow: resolve one group, then call ``delete_object()`` and
execute. Microsoft 365 groups are soft-deleted (kept in the deleted-items
container for 30 days and restorable); security groups are removed permanently.

For cleaning up many groups at once, see ``delete_batch.py``.

Requires application permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/group-delete
"""

from __future__ import annotations

import argparse

from office365.directory.groups.group import Group
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def find_group(client: GraphClient, name: str) -> Group | None:
    """Resolve a group by exact display name (``None`` when there is no match)."""
    escaped = name.replace("'", "''")
    groups = client.groups.filter(f"displayName eq '{escaped}'").get().execute_query()
    return groups[0] if groups else None


def main():
    parser = argparse.ArgumentParser(description="Delete a single group by display name")
    parser.add_argument("--name", required=True, help="exact display name of the group to delete")
    parser.add_argument("--permanent", action="store_true", help="delete permanently (default: soft delete)")
    parser.add_argument("--apply", action="store_true", help="actually delete (default: dry-run)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    group = find_group(client, args.name)
    if group is None:
        print(f"No group named '{args.name}'.")
        return

    kind = "Microsoft 365" if group.group_types else "Security"
    print(f"Found {kind} group '{group.display_name}' (id: {group.id}).")

    if not args.apply:
        print(f"Dry run — nothing deleted. Re-run with --apply to delete '{group.display_name}'.")
        return

    group.delete_object(permanent_delete=args.permanent).execute_query()
    mode = "permanently" if args.permanent else "soft"
    print(f"Group '{group.display_name}' {mode} deleted.")


if __name__ == "__main__":
    main()
