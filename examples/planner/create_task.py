"""
Create a new task in a plan and optionally assign it to a bucket.

Shows how to resolve a plan and bucket by name, then create a task
with those references.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-post-tasks
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
if len(plans) == 0:
    sys.exit("No plans were found")

plan = plans[0]
buckets = plan.buckets.get().execute_query()
bucket = buckets[0] if len(buckets) > 0 else None

task = client.planner.tasks.add("Update client list", plan.id, bucket.id if bucket else None).execute_query()
print(f"Task created: {task.title}  (ID: {task.id})")

if bucket:
    print(f"  Bucket: {bucket.name}")
