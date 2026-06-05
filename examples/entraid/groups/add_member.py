"""
Add and remove group members.

Demonstrates how to add a user to a group and remove them again.

https://learn.microsoft.com/en-us/graph/api/group-post-members

https://learn.microsoft.com/en-us/graph/api/resources/group

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

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# create a group and a user to work with
group = client.groups.create_security(
    create_unique_name("SecurityGroup"),
    description="Demo group for member management",
).execute_query()

user = client.users.get_by_principal_name("user@contoso.onmicrosoft.com")

# add the user as a member
group.members.add(user).execute_query()
print(f"User added to group '{group.display_name}'")

# clean up: remove the user from the group
group.members.remove(user).execute_query()
print(f"User removed from group '{group.display_name}'")

# clean up the group
group.delete_object(True).execute_query()
print("Group cleaned up.")
