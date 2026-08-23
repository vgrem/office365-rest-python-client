"""
Delete Microsoft 365 groups.

Notes:

    - Group.delete_object() Microsoft 365 groups are moved to a temporary container and can be restored within 30 days
    - Group.delete_object(permanent_delete=True) Microsoft 365 permanently deleted

https://learn.microsoft.com/en-us/graph/api/group-delete

Requires delegated permission ``Group.ReadWrite.All``.
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Delete Microsoft 365 groups")
    parser.add_argument("--permanent", action="store_true", help="delete permanently (default: soft delete)")
    parser.add_argument("--dry-run", action="store_true", help="list groups without deleting")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    groups = client.groups.filter("groupTypes/any(g:g eq 'Unified')").get().execute_query()

    print(f"Found {len(groups)} Microsoft 365 groups.")
    if args.dry_run:
        for g in groups:
            print(f"  {g.display_name}")
        return

    for i, group in enumerate(groups, start=1):
        print(f"({i} of {len(groups)}) Deleting {group.display_name} group ...")
        group.delete_object(permanent_delete=args.permanent).execute_query()
        mode = "permanently" if args.permanent else "soft"
        print(f"Group {mode} deleted.")


if __name__ == "__main__":
    main()
