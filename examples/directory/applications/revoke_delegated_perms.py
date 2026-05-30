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

client.revoke_delegated_permissions(test_client_id, scope).execute_query()
print(f"Requested revocation for scope '{scope}'.")
