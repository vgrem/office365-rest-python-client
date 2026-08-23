"""
Unfollow a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-unfollow
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Unfollow a SharePoint site")
    parser.add_argument("--site-url", required=True, help="Site URL")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    site_url = args.site_url.strip()
    site = client.sites.get_by_url(site_url).get().execute_query()
    client.me.unfollow_site(site).execute_query()
    print(f"Unfollowed {site.display_name}.")


if __name__ == "__main__":
    main()
