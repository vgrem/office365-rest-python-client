"""
List all apps available in the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="List apps in the tenant app catalog").parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    apps = ctx.web.tenant_app_catalog.available_apps.get().execute_query()
    for app in apps:
        print(f"  {app.title}  (ID: {app.id})")
    print(f"Total: {len(apps)} app(s)")


if __name__ == "__main__":
    main()
