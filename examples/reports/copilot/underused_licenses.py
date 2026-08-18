"""
Find users assigned a Copilot license who haven't signed in recently.

Cross-references Copilot SKUs with per-user license assignments and last
sign-in activity to identify underused (or unused) Copilot licenses.

Requires delegated permissions ``Organization.Read.All`` and ``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-list
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

COPILOT_KEYWORDS = ("COPILOT", "M365COPILOT", "CHAT")


def main():
    parser = argparse.ArgumentParser(description="Find underused Copilot licenses")
    parser.add_argument("--days", type=int, default=30, help="No-sign-in threshold in days")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # 1. Find Copilot SKU ids
    sku_ids = {
        s.sku_id
        for s in client.subscribed_skus.get().execute_query()
        if s.sku_part_number and any(k in s.sku_part_number.upper() for k in COPILOT_KEYWORDS)
    }
    if not sku_ids:
        print("No Copilot SKUs found in the tenant")
        return

    # 2. Find users with a Copilot SKU and no recent sign-in
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    users = (
        client.users.select(["displayName", "userPrincipalName", "assignedLicenses", "signInActivity"])
        .get()
        .execute_query()
    )

    print(f"Users with Copilot licenses but no sign-in for {args.days}+ days:\n")
    found = 0
    for u in users:
        assigned = u.assigned_licenses or []
        if not any(lic.skuId in sku_ids for lic in assigned):
            continue
        last = u.sign_in_activity.lastSignInDateTime
        if last is None or (isinstance(last, datetime) and last < cutoff):
            found += 1
            print(f"  {u.user_principal_name:40s}  last sign-in: {last or 'never'}")

    print(f"\n{found} underused Copilot license(s)")


if __name__ == "__main__":
    main()
