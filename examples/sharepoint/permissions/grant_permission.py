"""
Grant a role to a user or group on a site, list, folder, or file.

Requires Site Owner on the target scope.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.securable_object import SecurableObject
from office365.sharepoint.sharing.role_type import RoleType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ROLES = {
    "reader": RoleType.Reader,
    "contributor": RoleType.Contributor,
    "designer": RoleType.WebDesigner,
    "editor": RoleType.Editor,
    "admin": RoleType.Administrator,
}


def _resolve_scope(ctx: ClientContext, args: argparse.Namespace) -> SecurableObject:
    try:
        return ctx.web.get_securable_object(args.scope, list_title=args.list_title, url=args.url)
    except ValueError as e:
        sys.exit(str(e))


def main():
    parser = argparse.ArgumentParser(description="Grant a role to a user/group")
    parser.add_argument(
        "--scope",
        choices=["site", "list", "folder", "file"],
        required=True,
        help="permission scope (site, list, folder, file)",
    )
    parser.add_argument("--list", dest="list_title", default=None, help="list title (for --scope list)")
    parser.add_argument("--url", default=None, help="server-relative URL (for --scope folder/file)")
    parser.add_argument("--principal", required=True, help="user login/UPN or group name")
    parser.add_argument("--role", choices=sorted(ROLES), default="contributor", help="role to assign")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target = _resolve_scope(ctx, args)
    target.grant_access(args.principal, ROLES[args.role]).execute_query()
    print(f"✓ Granted '{args.role}' to {args.principal} on {args.scope}")


if __name__ == "__main__":
    main()
