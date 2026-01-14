"""
List the directory roles for the user.

https://learn.microsoft.com/en-us/graph/api/directoryrole-list?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

directory_roles = client.directory_roles.get().execute_query()
role_template_map = {role.properties.get("roleTemplateId"): role for role in directory_roles}

memberships = client.me.member_of.get().execute_query()
user_roles = []
for item in memberships:
    role_id = item.properties.get("roleTemplateId")
    if role_id and role_id in role_template_map:
        user_roles.append(role_template_map[role_id])


# Print roles the user is assigned to
for role in user_roles:
    print(f"User has role: {role.display_name}")
