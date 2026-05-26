"""
Revoke a delegated permission (OAuth2 scope) grant.

Useful when a user-specific consent grant is blocking the creation of an
admin-consented (AllPrincipals) grant. Run this first, then grant the
permission again with ``grant_delegated_perms.py``.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph
"""

from office365.graph_client import GraphClient
from tests import test_admin_principal_name, test_client_id, test_tenant

scope = input("Permission scope: ")

client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

# Find the service principal object ID for this app
sp = client.service_principals.get_by_app(test_client_id).get().execute_query()
assert sp.id is not None

# Query by clientId (scope is not filterable in Graph)
all_grants = client.oauth2_permission_grants.get().filter(
    f"clientId eq '{sp.id}'"
).execute_query()

# Filter by scope in Python
grants = [g for g in all_grants if g.scope == scope]

if not grants:
    print(f"❌ No grant found for scope '{scope}'.")
else:
    for g in grants:
        g.delete_object().execute_query()
    print(f"✅ Deleted {len(grants)} grant(s) for scope '{scope}'.")
