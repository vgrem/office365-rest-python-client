"""
Get device registration policy.

Retrieves the tenant-wide policy that controls device registration
settings — including whether users can join devices to Azure AD.

https://learn.microsoft.com/en-us/graph/api/deviceregistrationpolicy-get

https://learn.microsoft.com/en-us/graph/api/resources/deviceregistrationpolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

policy = client.policies.device_registration_policy.get().execute_query()

props = policy.properties
print(f"   Azure AD Join: {props.get('userDeviceQuota', 'N/A')}")
print(f"  Allowed to join: {props.get('azureADJoin', 'N/A')}")
print(f"Multi-factor auth config: {props.get('multiFactorAuthConfiguration', 'N/A')}")
