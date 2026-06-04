"""
Create a security group.

Unlike Microsoft 365 groups, security groups are used for managing
access to resources (apps, SharePoint sites, devices, etc.) and
do not have a mailbox or calendar.

https://learn.microsoft.com/en-us/graph/api/group-post-groups

https://learn.microsoft.com/en-us/graph/api/resources/groups-overview

Requires delegated permission ``Group.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

group = client.groups.create_security(
    create_unique_name("SecurityGroup"),
    description="Access control for Project Alpha",
).execute_query()
print(f"Security group created: {group.display_name} (id: {group.id})")

# clean up
group.delete_object(True).execute_query()
print("Group cleaned up.")
