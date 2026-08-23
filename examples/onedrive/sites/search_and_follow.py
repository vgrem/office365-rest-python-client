"""
Search and follow SharePoint sites.

Requires delegated permission ``Sites.Read.All``, ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-search
https://learn.microsoft.com/en-us/graph/api/user-followsite
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant, user_principal


def main():
    parser = argparse.ArgumentParser(description="Search and follow SharePoint sites")
    parser.add_argument("--keyword", default="team", help="search keyword")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    # 1. Search sites by keyword
    results = client.sites.search(args.keyword).execute_query()
    print(f"Sites matching '{args.keyword}' ({len(results)}):")
    for s in results:
        print(f"  {s.display_name:40s}  {s.web_url}")

    # 2. Follow a site
    user = client.users[user_principal]
    sites = results
    if len(sites) > 0:
        user.follow_site(sites[0]).execute_query()
        print(f"\nFollowed: {sites[0].display_name}")


if __name__ == "__main__":
    main()
