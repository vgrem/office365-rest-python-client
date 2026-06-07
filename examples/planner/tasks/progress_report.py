"""
Progress report: scan all tasks across all plans for the signed-in user
and build a status dashboard — counts by progress, priority, and
assignee.

Requires delegated permission ``Tasks.Read`` or ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planneruser-list-plans
https://learn.microsoft.com/en-us/graph/api/plannerplan-list-tasks
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

my_plans = client.me.planner.plans.get().execute_query()

by_progress = {0: 0, 25: 0, 50: 0, 75: 0, 100: 0}
by_priority = {}
total = 0

print("Task progress dashboard\n")

for plan in my_plans:
    tasks = plan.tasks.get().execute_query()
    if len(tasks) == 0:
        continue

    print(f"  📋 {plan.title}  ({len(tasks)} tasks)")

    for task in tasks:
        pct = task.percent_complete or 0
        priority = task.priority or 5
        by_progress[pct] = by_progress.get(pct, 0) + 1
        by_priority[priority] = by_priority.get(priority, 0) + 1
        total += 1

        assignees = []
        if task.assignments:
            for uid, details in task.assignments.items():
                assignees.append(uid[:8])

        print(f"     [{pct:3d}%] P{priority}  {task.title}")
        if assignees:
            print(f"           assignees: {', '.join(assignees)}")

    print()

print(f"Total: {total} tasks across {len(my_plans)} plans\n")

print("By progress:")
for pct in [0, 25, 50, 75, 100]:
    count = by_progress.get(pct, 0)
    bar = "█" * (count // 2) if count else ""
    print(f"  {pct:3d}%: {count:3d}  {bar}")

print("\nBy priority:")
for p in sorted(by_priority.keys()):
    count = by_priority[p]
    bar = "█" * (count // 2) if count else ""
    print(f"  P{p}: {count:3d}  {bar}")
