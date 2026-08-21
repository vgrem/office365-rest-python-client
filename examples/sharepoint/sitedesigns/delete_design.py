"""
Delete a site design by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Delete a site design")
    parser.add_argument("--design-id", required=True, help="site design id")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
    target = next((d for d in designs.value if str(d.Id) == args.design_id), None)
    if target is None:
        sys.exit(f"Site design not found: {args.design_id}")

    SiteScriptUtility.delete_site_design(ctx, str(target.Id)).execute_query()
    print(f"Deleted site design: {target.Title} (ID: {target.Id})")


if __name__ == "__main__":
    main()
