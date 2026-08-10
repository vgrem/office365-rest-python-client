"""Promote or demote a site page as news.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Promote or demote a site page as news")
    parser.add_argument("--file-name", required=True, help="page file name, e.g. Home.aspx")
    parser.add_argument("--demote", action="store_true", help="demote from news instead of promoting")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    page = ctx.site_pages.pages.get_by_name(args.file_name).get().execute_query()

    if args.demote:
        page.demote_from_news().execute_query()
        print(f"Page demoted from news: {args.file_name}")
    else:
        page.promote_to_news().execute_query()
        print(f"Page promoted to news: {args.file_name}")


if __name__ == "__main__":
    main()
