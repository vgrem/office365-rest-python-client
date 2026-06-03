"""
Create a new planner plan owned by a Microsoft 365 group.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-post-plans?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
group = client.groups.get_by_name("My Sample Team")
plan = client.planner.plans.add("My Plan", group).execute_query()
print(f"Plan created: {plan.title}  (ID: {plan.id})")
