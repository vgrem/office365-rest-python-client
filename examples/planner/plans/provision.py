"""
Provision a complete plan from a template: plan, category labels, buckets,
tasks, and assignments — in one flow.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-post-plans
https://learn.microsoft.com/en-us/graph/api/planner-post-buckets
https://learn.microsoft.com/en-us/graph/api/planner-post-tasks
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

# — Plan template —
CATEGORIES = {
    "category1": "Critical",
    "category2": "Client",
    "category3": "Internal",
}

BUCKETS = ["Backlog", "In Progress", "Review", "Done"]

TASKS = [
    {"title": "Kick-off meeting", "bucket": "Backlog", "category": "category3", "priority": 5},
    {"title": "Design review", "bucket": "Backlog", "category": "category2", "priority": 3},
    {"title": "API integration", "bucket": "Backlog", "category": "category1", "priority": 1},
]

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# Resolve group
group = client.groups.get_by_name("My Sample Team").get().execute_query()

# Create plan
plan = client.planner.plans.add(create_unique_name("Sprint 7"), group).execute_query()
print(f"Plan created: {plan.title}")

# Set category labels
details = plan.details.get().execute_query()
details.set_property("categoryDescriptions", CATEGORIES).update().execute_query()
print("  Categories: Critical, Client, Internal")

# Create buckets
bucket_map = {}
for name in BUCKETS:
    bucket = plan.buckets.add(name).execute_query()
    bucket_map[name] = bucket.id
    print(f"  Bucket: {name}")

# Create tasks
user = client.users.get_by_principal_name(test_user_principal_name).get().execute_query()

for spec in TASKS:
    task = client.planner.tasks.add(
        spec["title"],
        plan.id,
        bucket_map[spec["bucket"]],
    ).execute_query()

    # Set priority
    task.set_property("priority", spec["priority"])

    # Assign to user
    task.set_property(
        "assignments",
        {
            user.id: {
                "@odata.type": "#microsoft.graph.plannerAssignment",
                "orderHint": " !",
            }
        },
    )

    task.update().execute_query()
    print(f"  Task: {spec['title']}  (P{spec['priority']}, assigned)")

print(f"\nDone. Plan URL: https://tasks.office.com/{test_tenant}/Planner/Plan.aspx?plan={plan.id}")
