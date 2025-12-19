"""
Delete group

Notes:

    - Group.delete_object() Microsoft 365 groups are moved to a temporary container and can be restored within 30 days
    - Group.delete_object(permanent_delete=True) Microsoft 365 permanently deleted

https://learn.microsoft.com/en-us/graph/api/group-delete?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

# client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
# groups = client.groups.get().top(100).execute_query()
groups = client.groups.filter("groupTypes/any(g:g eq 'Unified')").get().execute_query()
deletedCount = 0
groups_count = len(groups)
while len(groups) > 0:
    cur_grp = groups[0]
    print(f"({deletedCount + 1} of {groups_count}) Deleting {cur_grp.display_name} group ...")
    cur_grp.delete_object(permanent_delete=True).execute_query()
    print("Group deleted permanently.")
    deletedCount += 1
