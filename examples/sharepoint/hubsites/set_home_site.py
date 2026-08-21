"""
Set a site as the landing (home) site for your intranet.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Sets a site as the home site").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site = ctx.site
    site.set_as_home_site().execute_query()
    print(f"Home site set: {site_url}")


if __name__ == "__main__":
    main()
