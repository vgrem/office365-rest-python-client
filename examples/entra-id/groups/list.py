"""
List groups.

https://learn.microsoft.com/en-us/graph/api/group-list?view=graph-rest-1.0

https://learn.microsoft.com/en-us/graph/api/resources/group

Requires delegated permission ``Group.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
groups = client.groups.get().top(100).execute_query()
for grp in groups:
    print(grp)
