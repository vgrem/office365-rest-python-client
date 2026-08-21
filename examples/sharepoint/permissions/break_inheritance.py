"""
Break permission inheritance on a site, list, or folder (unique permissions).

Requires Site Owner on the target scope.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.securable_object import SecurableObject
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


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
    sys.exit(f"Unsupported scope: {args.scope}")


def main():
    parser = argparse.ArgumentParser(description="Break permission inheritance")
    parser.add_argument(
        "--scope", choices=["site", "list", "folder"], required=True, help="permission scope (site, list, folder)"
    )
    parser.add_argument("--list", dest="list_title", default=None, help="list title (for --scope list)")
    parser.add_argument("--url", default=None, help="server-relative URL (for --scope folder)")
    parser.add_argument("--copy", action="store_true", help="copy parent role assignments first")
    parser.add_argument("--clear-subscopes", action="store_true", help="remove unique permissions from children")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target = _resolve_scope(ctx, args)
    target.break_role_inheritance(copy_role_assignments=args.copy, clear_sub_scopes=args.clear_subscopes).execute_query()
    print(f"✓ Broken permission inheritance on {args.scope}")


if __name__ == "__main__":
    main()
