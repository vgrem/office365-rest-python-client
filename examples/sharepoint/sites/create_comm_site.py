"""
Create a modern SharePoint communication site.

Requires SharePoint Administrator.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a modern communication site")
    parser.add_argument("--alias", required=True, help="site alias (defines the URL)")
    parser.add_argument("--title", required=True, help="site title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site = ctx.create_communication_site(alias=args.alias, title=args.title).execute_query()
    print(f"✓ Communication site created: {site.url}")


if __name__ == "__main__":
    main()
