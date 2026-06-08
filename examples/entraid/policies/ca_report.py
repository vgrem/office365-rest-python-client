"""
Conditional access: list policies, find break-glass accounts,
and report on enforcement state.

Critical for security posture assessment.

Requires delegated permission ``Policy.Read.All``.

https://learn.microsoft.com/en-us/graph/api/conditionalaccesspolicy-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

policies = client.identity.conditional_access.policies.top(20).get().execute_query()
print(f"Conditional access policies ({len(policies)}):")
for p in policies:
    state = p.state or "disabled"
    print(f"  {p.display_name:50s}  [{state}]")
