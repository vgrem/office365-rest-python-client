"""
List all tasks in a planner plan or a specific bucket.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-list-tasks?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
if len(plans) == 0:
    sys.exit("No plans were found")

tasks = plans[0].tasks.get().execute_query()
print(f"Tasks in plan '{plans[0].title}':")
for task in tasks:
    pct = task.percent_complete or 0
    priority = task.priority or 5
    print(f"  [{pct:3d}%] (P{priority}) {task.title}")
