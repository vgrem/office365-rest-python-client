"""
Assign an Entra ID directory role (e.g., Security Administrator) to a user.

If the role hasn't been activated in the tenant yet, it will be activated first.

Requires a privileged admin account with Global Administrator or
Privileged Role Administrator role.

Usage:
    python -m examples.directory.roles.assign_role

https://learn.microsoft.com/en-us/graph/api/directoryrole-post-members
"""

import sys

from office365.directory.permissions.guard import has_role
from office365.graph_client import GraphClient
from office365.runtime.types.exceptions import NotFoundException
from tests import test_admin_principal_name, test_client_id, test_tenant

privileged_client = GraphClient(tenant=test_tenant).with_token_interactive(
    test_client_id, test_admin_principal_name
)

if not has_role(privileged_client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator to assign roles.")
    sys.exit(1)

# 1. Pick a role by display name
role_name = input("Role to assign (e.g. 'Security Administrator'): ")

try:
    role = privileged_client.directory_roles.get_by_name(role_name).get().execute_query()
    print(f"✅ Found activated role '{role_name}'")
except NotFoundException:
    # Role not activated — look up its template ID from directory_role_templates
    templates = privileged_client.directory_role_templates.get().execute_query()
    template = next((t for t in templates if t.display_name == role_name), None)
    if template is None:
        print(f"❌ Unknown role '{role_name}'.")
        sys.exit(1)
    print(f"   Activating '{role_name}'...")
    role = privileged_client.directory_roles.add(roleTemplateId=template.id).execute_query()
    print("   ✅ Activated.")

# 2. Target user
user_upn = input("Target user UPN (e.g. 'user@contoso.com'): ")
user = privileged_client.users.get_by_principal_name(user_upn).get().execute_query()
assert user.id is not None

# 3. Assign
role.members.add(user).execute_query()
print(f"✅ Role '{role.display_name}' assigned to {user_upn}")
