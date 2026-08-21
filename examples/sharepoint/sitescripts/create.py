"""
Creates a site script that applies a custom theme.

Site scripts are used with site designs to apply customizations
to SharePoint sites.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a site script that applies a custom theme")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--script-name", default="Contoso theme script", help="site script name")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )

    site_script = {
        "$schema": "schema.json",
        "actions": [{"verb": "applyTheme", "themeName": "Contoso Theme"}],
        "bindata": {},
        "version": 1,
    }

    result = SiteScriptUtility.create_site_script(ctx, args.script_name, "", site_script).execute_query()
    print(json.dumps(result.value.to_json(), indent=4))


if __name__ == "__main__":
    main()
