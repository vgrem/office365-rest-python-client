"""
List device compliance policies in Intune.

Requires delegated permission ``DeviceManagementConfiguration.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-devicecompliancepolicy-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

policies = client.device_management.device_compliance_policies.get().execute_query()
for p in policies:
    print(f"  {p.display_name:40s}  platform: {p.platform or 'N/A'}")
