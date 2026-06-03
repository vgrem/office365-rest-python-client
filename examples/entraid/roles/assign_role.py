"""
Assign an Entra ID directory role (e.g., Security Administrator) to a user.

If the role hasn't been activated in the tenant yet, it will be activated first.

Requires a privileged admin account with Global Administrator or
Privileged Role Administrator role.

https://learn.microsoft.com/en-us/graph/api/directoryrole-post-members
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import DuplicatedObjectException
from office365.runtime.types.exceptions import NotFoundException
from tests import test_admin_principal_name, test_client_id, test_tenant

privileged_client = GraphClient(tenant=test_tenant).with_token_interactive(test_client_id, test_admin_principal_name)

if not has_role(privileged_client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator to assign roles.")
    sys.exit(1)

# 1. Pick a role by display name
role_name = input("Role to assign (e.g. 'Security Administrator'): ")

# 2. Activate the role (idempotent — DuplicatedObjectException means already active)
try:
    privileged_client.directory_roles.assign(role_name).execute_query()
except DuplicatedObjectException:
    pass

# 3. Get the activated role
try:
    role = privileged_client.directory_roles.get_by_name(role_name).execute_query()
except NotFoundException:
    print(f"❌ Role '{role_name}' not found after activation.")
    sys.exit(1)

# 4. Assign to user
user_upn = input("Target user UPN (e.g. 'user@contoso.com'): ")
role.add_member(user_upn).execute_query()
print(f"✅ Role '{role.display_name}' assigned to {user_upn}")
