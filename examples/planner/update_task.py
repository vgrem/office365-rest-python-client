"""
Update a planner task (title, due date, priority, percent complete).

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-update-tasks?view=graph-rest-1.0
"""

import sys
from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
if len(plans) == 0:
    sys.exit("No plans were found")

tasks = plans[0].tasks.get().execute_query()
if len(tasks) == 0:
    sys.exit("No tasks were found")

task = tasks[0]
task.set_property("title", f"{task.title} (updated)")
task.set_property("dueDateTime", (datetime.utcnow() + timedelta(days=7)).isoformat())
task.set_property("priority", 3)
task.set_property("percentComplete", 25)
task.update().execute_query()
print(f"Task updated: {task.title}  due: {task.due_datetime}  P{task.priority}")
