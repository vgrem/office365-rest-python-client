"""
Stale site lifecycle management — identify inactive sites, resolve
owners, archive candidates, and schedule deletion.

Real workflow used by SharePoint admins to manage site sprawl:
  1. Find sites with no recent activity (via analytics)
  2. Resolve site owners (via permissions API)
  3. Print a cleanup report with owner contacts
  4. Optionally archive or delete confirmed stale sites

Requires delegated permissions Sites.Read.All, Sites.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/itemanalytics-get
https://learn.microsoft.com/en-us/graph/api/site-list-permissions
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(
        description="Stale site lifecycle management — identify inactive sites, resolve owners, and optionally delete"
    )
    parser.add_argument("--inactivity-days", type=int, default=180, help="days of inactivity threshold")
    parser.add_argument("--delete", action="store_true", help="delete the stale sites (default is report only)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    print(f"Scanning sites for inactivity ({args.inactivity_days}+ days)...\n")

    stale = []
    for site in client.sites.get().execute_query():
        try:
            analytics = site.analytics.get().select(["allTime"]).execute_query()
            stat = analytics.all_time
            total = (stat.access.actionCount or 0) + (stat.edit.actionCount or 0) + (stat.create.actionCount or 0)
            if total > 0:
                continue
        except Exception:
            pass

        owners = []
        try:
            for p in site.permissions.get().execute_query():
                for identity in p.granted_to_identities:
                    if identity.user and "owner" in p.roles:
                        owners.append((identity.user or ""))
        except Exception:
            pass

        stale.append((site, owners))

    print(f"Stale sites: {len(stale)}\n")
    for site, owners in stale:
        owner_info = "; ".join(f"{n} ({e})" for n, e in owners) if owners else "NO OWNERS"
        print(f"  {site.display_name:45s}  owners: {owner_info}")

    if stale and args.delete:
        for site, _ in stale:
            site.delete_object().execute_query()
            print(f"  Deleted: {site.display_name}")
        print(f"\nDeleted {len(stale)} sites.")


if __name__ == "__main__":
    main()
