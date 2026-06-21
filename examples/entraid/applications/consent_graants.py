"""
Review OAuth consent grants — which apps have user-consented permissions
to access tenant data.

OAuth consent grants allow applications to act on behalf of users.
Unreviewed grants are a common source of shadow IT and data exposure.

Required delegated permissions:
    DelegatedPermissionGrant.Read.All

https://learn.microsoft.com/en-us/graph/api/resources/oauth2permissiongrant
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

grants = client.oauth2_permission_grants.get().execute_query()
print(f"OAuth consent grants ({len(grants)}):\n")

admin_count = 0
user_count = 0
for g in grants:
    scope = g.scope or ""
    consent_type = g.consent_type or "Unknown"
    if consent_type == "AllPrincipals":
        admin_count += 1
    else:
        user_count += 1
    print(f"  client={g.client_id}  scope={scope[:50]:50s}  type={consent_type}")

print(f"\nAdmin-consented (all users):  {admin_count}")
print(f"User-consented (individual):  {user_count}")
if user_count:
    print("\nUser-consented grants need individual review — each represents")
    print("a user authorizing an app to access their data.")
