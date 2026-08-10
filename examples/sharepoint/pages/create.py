"""Create a modern page on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create a modern page")
    parser.add_argument("--title", default=create_unique_name("Site Page "), help="page title (default: generated)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
    page = ctx.site_pages.create_page(args.title).execute_query()
    print(f"Page created: {page.absolute_url}")


if __name__ == "__main__":
    main()
