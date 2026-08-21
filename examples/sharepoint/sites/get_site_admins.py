"""
List the site collection administrators for a SharePoint site.

Uses the tenant admin context. Requires SharePoint Administrator.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List site collection administrators")
    parser.add_argument("--site-url", default=None, help="target site (default: {})".format(site_url))
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    admin = Tenant(ctx)
    target = args.site_url or site_url
    result = admin.get_site_administrators_by_site_url(target).execute_query()
    print(f"Site collection administrators for {target} ({len(result.value)}):")
    for info in result.value:
        print(f"  {info.name or '?'}  {info.email or info.loginName or '?'}")


if __name__ == "__main__":
    main()
