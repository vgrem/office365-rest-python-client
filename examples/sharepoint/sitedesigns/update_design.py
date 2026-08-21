"""
Update an existing site design — change title, description, or linked scripts.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Update a site design")
    parser.add_argument("--design-id", required=True, help="site design id")
    parser.add_argument("--description-suffix", default=" (updated)", help="text appended to the description")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
    target = next((d for d in designs.value if str(d.Id) == args.design_id), None)
    if target is None:
        sys.exit(f"Site design not found: {args.design_id}")

    update_info = SiteDesignMetadata()
    update_info.Id = target.Id
    update_info.Title = target.Title
    update_info.Description = f"{target.Description}{args.description_suffix}"
    update_info.WebTemplate = target.WebTemplate
    updated = SiteScriptUtility.update_site_design(ctx, update_info).execute_query()
    print(f"Updated: {updated.value.Title} — {updated.value.Description}")


if __name__ == "__main__":
    main()
