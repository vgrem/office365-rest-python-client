"""
List Conditional Access policies.

Lists all Conditional Access policies in the tenant, showing their
display name, state (enabled/disabled/report-only), and when they
were created.

https://learn.microsoft.com/en-us/graph/api/conditionalaccesspolicy-list

https://learn.microsoft.com/en-us/graph/api/resources/conditionalaccesspolicy

Requires delegated permission ``Policy.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

policies = client.policies.conditional_access_policies.get().execute_query()

for p in policies:
    state = p.properties.get("state", "")
    print(f"{p.display_name:50s}  {state:15s}  {p.created_datetime}")
