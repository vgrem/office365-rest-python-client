"""
Delete a planner plan by title.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-delete-plans?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
target = next((p for p in plans if p.title == "My Plan"), None)
if target is None:
    sys.exit("Plan not found")

target.delete_object().execute_query()
print(f"Plan '{target.title}' deleted")
