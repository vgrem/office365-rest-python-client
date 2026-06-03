"""
Assign a planner task to a user by email.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-update-tasks?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# Resolve user by email to get their ID
user = client.users.get_by_principal_name(test_user_principal_name).get().execute_query()

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
if len(plans) == 0:
    sys.exit("No plans were found")

tasks = plans[0].tasks.get().execute_query()
if len(tasks) == 0:
    sys.exit("No tasks were found")

task = tasks[0]
task.set_property("assignments", {user.id: {"@odata.type": "#microsoft.graph.plannerAssignment", "orderHint": " !"}})
task.update().execute_query()
print(f"Task '{task.title}' assigned to {user.user_principal_name}")
