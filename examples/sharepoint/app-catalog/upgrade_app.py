"""
Upgrade an app to a newer version available in the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upgrade an app in the tenant app catalog")
    parser.add_argument("--app-title", default="Starter Kit - Banner", help="app title in the catalog")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    app = ctx.web.tenant_app_catalog.available_apps.get_by_title(args.app_title).execute_query()
    if app.can_upgrade:
        app.deploy(skip_feature_deployment=False).execute_query()
        app.install().execute_query()
        print(f"Upgraded: {app.title}")
    else:
        print(f"No upgrade available for {app.title}")


if __name__ == "__main__":
    main()
