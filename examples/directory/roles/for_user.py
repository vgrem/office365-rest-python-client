"""
List the directory roles for the user.

https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)


result = client.me.get_directory_roles().execute_query()
# Print roles the user is assigned to
for role in result:
    print(f"User has role: {role.display_name}")
