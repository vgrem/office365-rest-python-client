"""
Register an existing site as a hub site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Registers a site as a hub site").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site = ctx.site
    site.register_hub_site().execute_query()
    print(f"Hub site registered: {site_url}")


if __name__ == "__main__":
    main()
