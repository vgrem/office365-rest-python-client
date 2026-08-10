"""Create and publish a modern page on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create and publish a modern page")
    parser.add_argument("--title", default=create_unique_name("Site Page "), help="page title (default: generated)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    page = ctx.site_pages.create_and_publish_page(args.title).execute_query()
    print(f"Published page: {page.absolute_url}")


if __name__ == "__main__":
    main()
