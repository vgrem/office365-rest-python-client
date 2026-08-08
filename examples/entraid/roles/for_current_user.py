"""
List the directory roles for the user.

https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)


me = client.me.get().execute_query()
print(f"Directory roles for {me}:")

result = client.me.get_directory_roles().execute_query()
for role in result:
    print(f"User has role: {role}")
