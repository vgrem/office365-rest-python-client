"""
Get metadata about a specific app in the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Inspect an app in the tenant app catalog")
    parser.add_argument("--app-title", default="Starter Kit - Banner", help="app title in the catalog")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    app = ctx.web.tenant_app_catalog.available_apps.get_by_title(args.app_title).execute_query()
    print(f"Title: {app.title}")
    print(f"Version: {app.app_catalog_version}")
    print(f"Can upgrade: {app.can_upgrade}")
    print(f"Is client-side: {app.is_client_side_solution}")
    print(f"AAD permissions: {app.aad_permissions}")


if __name__ == "__main__":
    main()
