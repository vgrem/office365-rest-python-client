"""
Get authentication methods policy.

Retrieves the tenant-wide policy that controls which authentication
methods users can register and use (MFA, SSPR, passwordless, etc.).

https://learn.microsoft.com/en-us/graph/api/authenticationmethodspolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethodspolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

policy = client.policies.authentication_methods_policy.get().execute_query()

print(f"   Description: {policy.properties.get('description', '')}")
print(f"  Display name: {policy.properties.get('displayName', '')}")
print(f"Migrate to MFA: {policy.properties.get('enableMigration', False)}")
