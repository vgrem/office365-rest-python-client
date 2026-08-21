"""
Resolves a web from an absolute resource (e.g. page) URL.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Resolve a web from an absolute page URL")
    parser.add_argument("--site-url", default=team_site_url, help="target site URL")
    args = parser.parse_args()

    page_abs_url = f"{args.site_url}/SitePages/Home.aspx"
    ctx = ClientContext.from_url(page_abs_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    web = ctx.web.get().execute_query()
    print(web.url)


if __name__ == "__main__":
    main()
