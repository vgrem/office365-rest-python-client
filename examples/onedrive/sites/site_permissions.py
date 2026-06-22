"""
List all users and groups with access to a specific site.

Requires delegated permission Sites.Read.All.

https://learn.microsoft.com/en-us/graph/api/site-list-permissions
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Sites.Read.All")
)

sites = client.sites.top(10).get().execute_query()
for site in sites:
    perms = site.permissions.get().execute_query()
    print(f"\nPermissions for {site.display_name} ({len(perms)}):")
    for p in perms:
        for identity in p.granted_to_identities:
            print(f"   {identity.user:35s}  roles={p.roles}")
        for identity in p.granted_to_identities_v2:
            user = identity.user or identity.group or identity.siteUser
            if user:
                print(f"  [GROUP] {user:30s}  roles={p.roles}")
