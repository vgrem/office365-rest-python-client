"""
Get cross-tenant access policy.

Retrieves the default cross-tenant access settings that control
inbound and outbound access to and from external Azure AD tenants.

https://learn.microsoft.com/en-us/graph/api/crosstenantaccesspolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/crosstenantaccesspolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

policy = client.policies.cross_tenant_access_policy.get().execute_query()

print("Cross-tenant access settings:")
print(f"  Default inbound: {policy.properties.get('defaultInbound', 'N/A')}")
print(f"  Default outbound: {policy.properties.get('defaultOutbound', 'N/A')}")
print(f"  Allowed cloud endpoints: {policy.allowed_cloud_endpoints}")
