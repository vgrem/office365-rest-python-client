"""
List Intune terms and conditions configured for the tenant.

Requires delegated permission ``DeviceManagementConfiguration.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-companyterms-termsandconditions-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

terms = client.device_management.terms_and_conditions.get().execute_query()
for t in terms:
    print(f"  {t.display_name:40s}  version: {t.version}")
