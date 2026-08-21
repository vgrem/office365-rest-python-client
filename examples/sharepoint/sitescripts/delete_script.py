"""
Delete a site script by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete a site script by ID")
    parser.add_argument("--site-url", default=site_url, help="target site URL")
    parser.add_argument("--script-id", default=None, help="site script id (default: first script)")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    result = SiteScriptUtility.get_site_scripts(ctx).execute_query()
    if not result.value:
        sys.exit("No site scripts found.")
    if args.script_id:
        target = next((s for s in result.value if str(s.Id) == args.script_id), None)
        if target is None:
            raise ValueError(f"Site script {args.script_id} not found")
    else:
        target = result.value[0]
    assert target.Id is not None
    SiteScriptUtility.delete_site_script(ctx, target.Id).execute_query()
    print(f"Deleted site script: {target.Title} (ID: {target.Id})")


if __name__ == "__main__":
    main()
