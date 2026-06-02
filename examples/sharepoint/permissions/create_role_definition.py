"""
Create a custom role definition (permission level).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.permissions.permission_kind import PermissionKind
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
perms = BasePermissions()
perms.set(PermissionKind.ViewListItems)
perms.set(PermissionKind.ViewListItems)

role = ctx.web.role_definitions.add(
    "Custom Reader",
    "Can view items but not edit",
    perms,
).execute_query()
print(f"Role created: {role.name}  (ID: {role.id})")
