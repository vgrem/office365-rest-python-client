"""
Get basic properties of the current SharePoint site.

Requires read access.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Get basic site properties").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    web = ctx.web.get().execute_query()
    print(f"Title:    {web.title}")
    print(f"URL:      {web.url}")
    print(f"Template: {web.web_template}")


if __name__ == "__main__":
    main()
