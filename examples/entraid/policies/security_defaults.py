"""
Get Microsoft Entra security defaults policy.

Retrieves the tenant-wide policy that controls whether security defaults
are enabled (recommended by default for new tenants).

https://learn.microsoft.com/en-us/graph/api/identitysecuritydefaultsenforcementpolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/identitysecuritydefaultsenforcementpolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = (
    GraphClient(tenant=tenant)
    .with_client_secret(client_id, client_secret)
    .require_application_permission("Policy.Read.All")
)

policy = client.policies.identity_security_defaults_enforcement_policy.get().execute_query()

print(f"Security defaults enabled: {policy.is_enabled}")
