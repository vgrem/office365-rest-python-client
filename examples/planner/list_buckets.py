"""
List all buckets in a planner plan.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/planner-list-buckets?view=graph-rest-1.0
"""

import sys

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

group = client.groups.get_by_name("My Sample Team").get().execute_query()
plans = group.planner.plans.get().execute_query()
if len(plans) == 0:
    sys.exit("No plans were found")

buckets = plans[0].buckets.get().execute_query()
for bucket in buckets:
    print(f"  {bucket.name}  (ID: {bucket.id})")
