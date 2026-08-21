"""
Remove an app from the tenant app catalog entirely.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Remove an app from the tenant app catalog")
    parser.add_argument("--app-title", default="Starter Kit - Banner", help="app title in the catalog")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    app = ctx.web.tenant_app_catalog.available_apps.get_by_title(args.app_title).execute_query()
    app.remove().execute_query()
    print(f"Removed: {app.title} from catalog")


if __name__ == "__main__":
    main()
