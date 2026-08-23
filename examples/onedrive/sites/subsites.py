"""
List subsites under a site collection.

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/site-list-subsites
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="List subsites under a site collection")
    parser.add_argument("--site-url", default=site_url, help="site collection URL")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Sites.Read.All")
    )

    site = client.sites.get_by_url(args.site_url).get().execute_query()
    subsites = site.sites.get().execute_query()
    print(f"Subsites of {site.display_name} ({len(subsites)}):")
    for s in subsites:
        print(f"  {s.display_name:40s}  {s.web_url}")


if __name__ == "__main__":
    main()
