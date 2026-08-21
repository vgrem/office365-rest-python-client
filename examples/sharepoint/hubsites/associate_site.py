"""
Associate a site with an existing hub site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Associates a site with a hub site").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    hub_sites = ctx.hub_sites.get().execute_query()
    if hub_sites:
        target = hub_sites[0]
        assert target.id is not None
        site = ctx.site
        site.join_hub_site(target.id).execute_query()
        print(f"Site associated to hub: {target.title}")


if __name__ == "__main__":
    main()
