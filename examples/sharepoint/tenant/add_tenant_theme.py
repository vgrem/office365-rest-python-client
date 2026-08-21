"""
Add a tenant theme.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.portal.theme_manager import ThemeManager
from tests.settings import admin_site_url, client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Add a tenant theme")
    parser.add_argument("--name", default="Contoso Theme", help="Theme name")
    args = parser.parse_args()

    ctx = ClientContext(admin_site_url).with_client_secret(tenant, client_id, client_secret)

    manager = ThemeManager(ctx)
    theme = {
        "themePrimary": "#0078d4",
        "themeLighterAlt": "#eff6fc",
        "themeLighter": "#deecf9",
    }
    manager.add_tenant_theme(args.name, json.dumps(theme)).execute_query()
    print(f"Theme added: {args.name}")


if __name__ == "__main__":
    main()
