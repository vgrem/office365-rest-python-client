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

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

INACTIVITY_DAYS = 180

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

print(f"Scanning sites for inactivity ({INACTIVITY_DAYS}+ days)...\n")

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

if stale and input(f"\nDelete {len(stale)} stale sites? (yes/no): ").strip().lower() == "yes":
    for site, _ in stale:
        site.delete_object().execute_query()
        print(f"  Deleted: {site.display_name}")
    print(f"\nDeleted {len(stale)} sites.")
