"""
Update site collection properties (title, description).

Requires Site Owner on the site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Update site properties")
    parser.add_argument("--title", default=None, help="new title")
    parser.add_argument("--description", default=None, help="new description")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    web = ctx.web.get().execute_query()
    if args.title:
        web.set_property("Title", args.title)
    if args.description is not None:
        web.set_property("Description", args.description)
    web.update().execute_query()
    print(f"✓ Site updated: {web.title}")


if __name__ == "__main__":
    main()
