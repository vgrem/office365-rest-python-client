"""
Restore a deleted SharePoint site (or list deleted sites for inspection).

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant


def main():
    parser = argparse.ArgumentParser(description="List or restore deleted sites")
    parser.add_argument("--restore", help="URL of a deleted site to restore (default: list only)")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    tenant_obj = Tenant(ctx)

    deleted = tenant_obj.get_deleted_site_properties().execute_query()
    print(f"Deleted sites ({len(deleted)}):")
    for site in deleted:
        print(f"  {site.url}")

    if args.restore:
        tenant_obj.restore_deleted_site(args.restore).execute_query()
        print(f"Restored: {args.restore}")


if __name__ == "__main__":
    main()
