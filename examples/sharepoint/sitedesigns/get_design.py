"""
Get metadata for a specific site design by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get site design metadata")
    parser.add_argument("--design-id", default=None, help="site design id (default: first design)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
    if not designs.value:
        sys.exit("No site designs found.")
    if args.design_id:
        target = next((d for d in designs.value if str(d.Id) == args.design_id), designs.value[0])
    else:
        target = designs.value[0]
    assert target.Id is not None

    detail = SiteScriptUtility.get_site_design_metadata(ctx, str(target.Id)).execute_query()
    print(f"Title:        {detail.value.Title}")
    print(f"Description:  {detail.value.Description}")
    print(f"WebTemplate:  {detail.value.WebTemplate}")
    print(f"SiteScriptIds:{detail.value.SiteScriptIds}")
    print(f"Id:           {detail.value.Id}")


if __name__ == "__main__":
    main()
