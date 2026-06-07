"""
Create sharing links and send sharing invitations for files.

Two sharing patterns: anonymous/organization links and
direct invitations to specific users.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-createlink
https://learn.microsoft.com/en-us/graph/api/driveitem-invite
"""

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

items = client.me.drive.root.children.top(1).get().execute_query()
if len(items) == 0:
    exit("No files found")

item = items[0]

# 1. Create an anonymous view link
link = item.create_link("view", "anonymous").execute_query()
print(f"Anonymous link: {link.link.web_url}")

# 2. Send a sharing invitation to a user
invite = item.invite(
    [test_user_principal_name],
    send_invitation=True,
    message="Here's the file you requested.",
).execute_query()
print(f"Invitation sent to: {test_user_principal_name}")

# 3. List current permissions
permissions = item.permissions.get().execute_query()
print(f"Permissions ({len(permissions)}):")
for p in permissions:
    roles = p.roles or []
    print(f"  ID: {p.id}  roles: {', '.join(roles)}")
