"""
A user's OneDrive — quota, usage, and storage state.

Shows how an administrator inspects a specific user's drive: who owns it, its
quota and current usage, and how much space is left. Useful for storage
troubleshooting and user support.

Requires delegated permission ``Files.Read.All`` and ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list-drive
https://learn.microsoft.com/en-us/graph/api/drive-get
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant, user_principal

GIB = 1024**3


def main():
    parser = argparse.ArgumentParser(description="Show a user's OneDrive drive and quota")
    parser.add_argument("--user", default=user_principal, help="user principal name (UPN) of the drive owner")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Files.Read.All", "Sites.Read.All")
    )

    drive = client.users[args.user].drive.get().execute_query()
    quota = drive.quota
    used = quota.used or 0
    total = quota.total or 0
    remaining = quota.remaining or 0
    pct = used / total * 100 if total else 0.0

    owner = drive.owner.user.displayName or args.user
    print(f"Drive of '{args.user}' ({owner}):")
    print(f"  id:            {drive.id}")
    print(f"  type:          {drive.drive_type}")
    print(f"  web URL:       {drive.web_url}")
    print(f"  used:          {used / GIB:.2f} GiB")
    print(f"  remaining:     {remaining / GIB:.2f} GiB")
    print(f"  total (quota): {total / GIB:.2f} GiB")
    print(f"  usage:         {pct:.1f}%")


if __name__ == "__main__":
    main()
