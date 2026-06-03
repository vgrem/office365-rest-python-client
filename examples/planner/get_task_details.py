"""
Get planner task details (description, checklist, references, preview type).

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-get-taskdetails?view=graph-rest-1.0
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
if len(tasks) == 0:
    sys.exit("No tasks were found")

task = tasks[0]
details = task.details.get().execute_query()
print(f"Task: {task.title}")
print(f"  Description: {details.description}")
print(f"  Preview type: {details.preview_type}")
if details.checklist:
    print(f"  Checklist items: {len(list(details.checklist))}")
