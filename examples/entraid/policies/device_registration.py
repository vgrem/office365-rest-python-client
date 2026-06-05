"""
Get device registration policy.

Retrieves the tenant-wide policy that controls device registration
settings — including whether users can join devices to Azure AD.

https://learn.microsoft.com/en-us/graph/api/deviceregistrationpolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/deviceregistrationpolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

policy = client.policies.device_registration_policy.get().execute_query()

props = policy.properties
print(f"   Azure AD Join: {props.get('userDeviceQuota', 'N/A')}")
print(f"  Allowed to join: {props.get('azureADJoin', 'N/A')}")
print(f"Multi-factor auth config: {props.get('multiFactorAuthConfiguration', 'N/A')}")
