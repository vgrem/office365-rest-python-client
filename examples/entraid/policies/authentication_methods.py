"""
Get authentication methods policy.

Retrieves the tenant-wide policy that controls which authentication
methods users can register and use (MFA, SSPR, passwordless, etc.).

https://learn.microsoft.com/en-us/graph/api/authenticationmethodspolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethodspolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

policy = client.policies.authentication_methods_policy.get().execute_query()

print(f"   Description: {policy.properties.get('description', '')}")
print(f"  Display name: {policy.properties.get('displayName', '')}")
print(f"Migrate to MFA: {policy.properties.get('enableMigration', False)}")
