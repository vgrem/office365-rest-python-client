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
from tests import test_admin_principal_name, test_client_id, test_tenant

# Common role template IDs (well-known, never change across tenants)
ROLE_TEMPLATES = {
    "Global Administrator": "62e90394-69f5-4237-9190-012177145e10",
    "Security Administrator": "194ae4cb-b126-40b2-bd5b-6091b380977d",
    "Security Reader": "5d6b6bb7-de71-4623-b4af-96380a352509",
    "SharePoint Administrator": "f28a1f50-f6e7-4571-818b-6a12f2af6b6c",
    "Exchange Administrator": "29232cdf-9323-42fd-ade2-1d097af3e4de",
    "Teams Administrator": "69091246-20e8-4a56-aa4d-066075b2a7a8",
    "Compliance Administrator": "17315797-102d-40b4-93e0-432062caca18",
    "User Administrator": "fe930be7-5e62-47db-91af-98c3a49a38b1",
    "Privileged Role Administrator": "e8611ab8-c189-46e8-94e1-60213ab1f814",
    "Global Reader": "f2ef992c-3afb-46b9-b7cf-a126ee74c451",
}

privileged_client = GraphClient(tenant=test_tenant).with_token_interactive(
    test_client_id, test_admin_principal_name
)

if not has_role(privileged_client, "Global Administrator", "Privileged Role Administrator"):
    print("❌ Need Global Administrator or Privileged Role Administrator to assign roles.")
    sys.exit(1)

# 1. List activated roles
print("Activated directory roles:")
roles = privileged_client.directory_roles.get().execute_query()
activated_names = {r.display_name for r in roles}
if not activated_names:
    print("  (none)")
else:
    for r in roles:
        print(f"  ✅ {r.display_name}")

# 2. Pick a role by name
print()
role_name = input("Role to assign (e.g. 'Security Administrator'): ")

template_id = ROLE_TEMPLATES.get(role_name)
if template_id is None:
    print(f"❌ Unknown role '{role_name}'. Add its template ID to ROLE_TEMPLATES.")
    sys.exit(1)

if role_name in activated_names:
    role = next(r for r in roles if r.display_name == role_name)
else:
    print(f"   Activating '{role_name}'...")
    role = privileged_client.directory_roles.add(roleTemplateId=template_id).execute_query()
    print("   ✅ Activated.")

# 3. Target user
user_upn = input("Target user UPN (e.g. 'user@contoso.com'): ")
user = privileged_client.users.get_by_principal_name(user_upn).get().execute_query()
assert user.id is not None

# 4. Assign
role.members.add(user).execute_query()
print(f"✅ Role '{role.display_name}' assigned to {user_upn}")
