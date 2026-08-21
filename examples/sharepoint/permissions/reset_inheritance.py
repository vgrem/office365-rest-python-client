"""
Reset permission inheritance on a site, list, or folder (revert to parent).

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
    parser = argparse.ArgumentParser(description="Reset permission inheritance")
    parser.add_argument(
        "--scope", choices=["site", "list", "folder"], required=True, help="permission scope (site, list, folder)"
    )
    parser.add_argument("--list", dest="list_title", default=None, help="list title (for --scope list)")
    parser.add_argument("--url", default=None, help="server-relative URL (for --scope folder)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target = _resolve_scope(ctx, args)
    target.reset_role_inheritance().execute_query()
    print(f"✓ Reset permission inheritance on {args.scope}")


if __name__ == "__main__":
    main()
