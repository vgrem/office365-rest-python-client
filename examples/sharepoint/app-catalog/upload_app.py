"""
Upload a SharePoint Framework solution (.sppkg) to the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Upload an app package to the tenant app catalog")
    parser.add_argument("--app-path", default="./react-banner.sppkg", help="path to the .sppkg file")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    app_file = ctx.web.tenant_app_catalog.app_from_path(args.app_path, True).execute_query()
    print(f"Uploaded: {app_file.name}")


if __name__ == "__main__":
    main()
