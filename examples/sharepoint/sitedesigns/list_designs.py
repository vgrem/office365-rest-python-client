"""
List all site designs available in the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="List site designs").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = SiteScriptUtility.get_site_designs(ctx).execute_query()
    for d in result.value:
        print(f"  {d.Title}  (ID: {d.Id}, WebTemplate: {d.WebTemplate})")
    print(f"Total: {len(result.value)} site design(s)")


if __name__ == "__main__":
    main()
