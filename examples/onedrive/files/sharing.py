"""
Create sharing links and send sharing invitations for files.

Two sharing patterns: anonymous/organization links and
direct invitations to specific users.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-createlink
https://learn.microsoft.com/en-us/graph/api/driveitem-invite
"""

import sys

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

items = client.me.drive.root.children.top(1).get().execute_query()
if len(items) == 0:
    sys.exit("No files found")

item = items[0]

# 1. Create an anonymous view link
link = item.create_link("view", "anonymous").execute_query()
print(f"Anonymous link: {link.link.webUrl}")

# 2. Send a sharing invitation to a user
invite = item.invite(
    [user_principal],
    send_invitation=True,
    message="Here's the file you requested.",
).execute_query()
print(f"Invitation sent to: {user_principal}")

# 3. List current permissions
permissions = item.permissions.get().execute_query()
print(f"Permissions ({len(permissions)}):")
for p in permissions:
    print(f"  ID: {p.id}  roles: {', '.join(p.roles)}")
