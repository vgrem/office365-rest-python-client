"""
Uninstall an app from a target site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Uninstall an app from a site")
    parser.add_argument("--app-title", default="Starter Kit - Banner", help="app title in the catalog")
    parser.add_argument("--site-url", default=team_site_url, help="target site URL")
    args = parser.parse_args()

    admin = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    app = admin.web.tenant_app_catalog.available_apps.get_by_title(args.app_title).execute_query()
    app.uninstall().execute_query()
    print(f"Uninstalled: {app.title} from {args.site_url}")


if __name__ == "__main__":
    main()
