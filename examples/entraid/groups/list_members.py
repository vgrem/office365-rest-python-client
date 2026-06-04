"""
List group members.

Lists all direct members of a group — includes users, service principals,
and nested groups.

https://learn.microsoft.com/en-us/graph/api/group-list-members

https://learn.microsoft.com/en-us/graph/api/resources/group

Requires delegated permission ``Group.Read.All`` or ``Group.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

group = client.groups.get_by_name("Marketing Team")
members = group.members.get().execute_query()

for m in members:
    print(f"{m.resource_type:<20s}  {m.display_name:40s}  {m.id}")
