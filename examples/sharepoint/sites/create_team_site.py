"""
Create a modern SharePoint team site (Microsoft 365 group-connected).

Requires SharePoint Administrator.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-creation-rest
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a modern team site")
    parser.add_argument("--alias", required=True, help="site alias (defines the URL)")
    parser.add_argument("--title", required=True, help="site title")
    parser.add_argument("--private", action="store_true", help="private (group-connected) site")
    parser.add_argument("--owner", default=None, help="initial owner UPN")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site = ctx.create_team_site(
        alias=args.alias, title=args.title, is_public=not args.private, owners=[args.owner] if args.owner else None
    ).execute_query()
    print(f"✓ Team site created: {site.url}")


if __name__ == "__main__":
    main()
