"""
List recently deleted users and restore one by id.

A recently deleted user remains available for up to 30 days before being
permanently deleted.

Requires delegated permission ``User.ReadWrite.All`` or ``Directory.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-list
https://learn.microsoft.com/en-us/graph/api/directory-deleteditems-restore
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List or restore deleted users")
    parser.add_argument("--restore", help="Id of a deleted user to restore (default: list only)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    deleted = client.directory.deleted_users.select(["id", "userPrincipalName"]).get().execute_query()
    print(f"Deleted users ({len(deleted)}):")
    for user in deleted:
        print(f"  {user.id}  {user.get_property('userPrincipalName') or '?'}")

    if args.restore:
        target = next((u for u in deleted if u.id == args.restore), None)
        if target is None:
            raise SystemExit(f"Deleted user '{args.restore}' not found")
        target.restore().execute_query()
        print(f"Restored: {target.get_property('userPrincipalName') or args.restore}")


if __name__ == "__main__":
    main()
