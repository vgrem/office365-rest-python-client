"""
Create a classic SharePoint site collection (not group-connected).

Uses the tenant admin context. Requires SharePoint Administrator.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a classic site collection")
    parser.add_argument("--url", required=True, help="site URL, e.g. https://contoso-admin.sharepoint.com/sites/Site")
    parser.add_argument("--owner", required=True, help="owner UPN")
    parser.add_argument("--title", default=None, help="site title")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    admin = Tenant(ctx)
    admin.create_site(args.url, args.owner, args.title).execute_query()
    print(f"✓ Classic site created: {args.url}")


if __name__ == "__main__":
    main()
