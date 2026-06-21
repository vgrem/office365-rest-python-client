"""
Audit external sharing across all sites — find sites shared with
users outside the organization.

Checks each site's permissions for guest users whose email domain
differs from the tenant domain.

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

tenant_domain = tenant.split("@")[-1] if "@" in tenant else tenant

sites = client.sites.get_all().execute_query()
print(f"Checking {len(sites)} sites for external sharing...\n")
found = False
for s in sites:
    perms = s.permissions.get().execute_query()
    for p in perms:
        for identity in p.granted_to_identities:
            user = identity.user
            if user and user.email and tenant_domain not in user.email:
                print(f"  {s.display_name:45s}  {user.display_name or '?':25s}  {user.email or '?'}")
                found = True
                break

if not found:
    print("No external sharing detected.")
