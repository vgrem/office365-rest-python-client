"""
Get hub sites that are connected to a specific hub site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Gets hub sites connected to a hub site").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    hub_sites = ctx.hub_sites.get().execute_query()
    if hub_sites:
        target = hub_sites[0]
        assert target.id is not None
        connected = ctx.hub_sites.get_connected_hubs(target.id, 1).execute_query()
        for hub in connected:
            print(f"{hub.title}  ({hub.site_url})")


if __name__ == "__main__":
    main()
