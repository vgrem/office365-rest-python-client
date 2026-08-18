"""
Connect via national clouds (Microsoft 365 GCC High environment).

Microsoft Graph for US Government L4: https://graph.microsoft.us

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/graph/deployments
"""

from office365.azure_env import AzureEnvironment
from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant, environment=AzureEnvironment.USGovernmentHigh).with_client_secret(
    client_id, client_secret
)
org = client.organization.get().execute_query()
for o in org:
    print(f"Organization: {o.properties.get('displayName')}")
