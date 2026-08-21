"""
Sets secondary site collection administrators on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Set secondary site collection administrators")
    parser.add_argument("--site-url", default=team_site_url, help="Site URL to set administrators on")
    args = parser.parse_args()

    ctx = Tenant.from_url(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    result = ctx.get_site_secondary_administrators_by_site_url(args.site_url).execute_query()

    user_result = ctx.context.search_user("SharePoint Service Administrator").execute_query()
    names = [admin.loginName for admin in result.value if admin.loginName is not None]
    user_name = user_result.value.get("loginName")
    if user_name is not None:
        names.append(user_name)
    ctx.set_site_secondary_administrators_by_site_url(site_url=args.site_url, names=names).execute_query()


if __name__ == "__main__":
    main()
