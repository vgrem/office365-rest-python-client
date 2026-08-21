"""
Delete a SharePoint site collection.

Uses the tenant admin context. Requires SharePoint Administrator.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete a SharePoint site")
    parser.add_argument("--url", required=True, help="site URL to delete")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    admin = Tenant(ctx)
    admin.remove_site(args.url).execute_query()
    print(f"✓ Site deleted: {args.url}")


if __name__ == "__main__":
    main()
