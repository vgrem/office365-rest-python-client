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

site_url = input("Site URL: ").strip()
site = client.sites.get_by_url(site_url).get().execute_query()

perms = site.permissions.get().execute_query()
print(f"\nPermissions for {site.display_name} ({len(perms)}):")
for p in perms:
    for identity in p.grantedToIdentities or []:
        user = identity.user
        role = p.roles or []
        print(f"  {user.display_name:30s}  {user.email:35s}  roles={role}")
    for identity in p.grantedToIdentitiesV2 or []:
        user = identity.user or identity.group or identity.siteUser
        if user:
            print(f"  [GROUP] {user.display_name:30s}  roles={p.roles}")
