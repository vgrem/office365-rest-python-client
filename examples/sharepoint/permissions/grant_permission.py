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
    if args.scope == "site":
        return ctx.web
    if args.scope == "list":
        if not args.list_title:
            sys.exit("--list <title> is required for --scope list")
        return ctx.web.lists.get_by_title(args.list_title)
    if args.scope == "folder":
        if not args.url:
            sys.exit("--url <server-relative-url> is required for --scope folder")
        return ctx.web.get_folder_by_server_relative_url(args.url).list_item_all_fields
    if args.scope == "file":
        if not args.url:
            sys.exit("--url <server-relative-url> is required for --scope file")
        return ctx.web.get_file_by_server_relative_url(args.url).listItemAllFields
    sys.exit(f"Unsupported scope: {args.scope}")


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
    target.add_role_assignment(args.principal, ROLES[args.role]).execute_query()
    print(f"✓ Granted '{args.role}' to {args.principal} on {args.scope}")


if __name__ == "__main__":
    main()
