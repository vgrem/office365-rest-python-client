"""
Find sites with no activity — combines analytics check with
owner resolution for a complete stale site audit.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/itemanalytics-get
https://learn.microsoft.com/en-us/graph/api/site-list-permissions
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

for site in client.sites.get().execute_query():
    try:
        analytics = site.analytics.get().execute_query()
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
                if identity.user and "owner" in list(p.roles):
                    owners.append((identity.user))
    except Exception:
        pass

    owner_info = "; ".join(f"{n} ({e})" for n, e in owners) if owners else "NO OWNERS"
    print(f"  {site.display_name:45s}  owners: {owner_info}")
