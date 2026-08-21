"""
List all site scripts in the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List all site scripts in the tenant")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    result = SiteScriptUtility.get_site_scripts(ctx).execute_query()
    for s in result.value:
        print(f"  {s.Title}  (ID: {s.Id}, Version: {s.Version})")
    print(f"Total: {len(result.value)} site script(s)")


if __name__ == "__main__":
    main()
