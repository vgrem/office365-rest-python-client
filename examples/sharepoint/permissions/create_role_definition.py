"""
Create a custom role definition (permission level).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.permissions.kind import PermissionKind
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a custom role definition")
    parser.add_argument("--name", default="Custom Reader", help="Role name")
    parser.add_argument("--description", default="Can view items but not edit", help="Role description")
    parser.add_argument("--keep", action="store_true", help="Keep the role (default: delete after demo)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    perms = BasePermissions()
    perms.set(PermissionKind.ViewListItems)
    perms.set(PermissionKind.ViewPages)

    role = ctx.web.role_definitions.add(perms, args.name, args.description).execute_query()
    print(f"Role created: {role.name}  (ID: {role.id})")

    if not args.keep:
        role.delete_object().execute_query()
        print("  (role removed after demo)")


if __name__ == "__main__":
    main()
