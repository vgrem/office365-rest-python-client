"""
Get presence for a single user.

Requires delegated permission Presence.Read.

https://learn.microsoft.com/en-us/graph/api/presence-get
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

presence = client.users[user_principal].presence.get().execute_query()
print(f"{user_principal}:  availability={presence.availability}  activity={presence.activity}")
