"""
Site-level governance inventory — content types and columns.

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/site-list-contenttypes
https://learn.microsoft.com/en-us/graph/api/site-list-columns
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Site-level governance inventory — content types and columns")
    parser.add_argument("--site-url", required=True, help="Site URL")
    args = parser.parse_args()

    client = (
        GraphClient(tenant=tenant)
        .with_client_secret(client_id, client_secret)
        .require_application_permission("Sites.Read.All")
    )

    site_url = args.site_url.strip()
    site = client.sites.get_by_url(site_url).get().execute_query()

    content_types = site.content_types.get().execute_query()
    print(f"Content types on {site.display_name} ({len(content_types)}):")
    for ct in content_types:
        print(f"  {ct.name}")

    columns = site.columns.get().execute_query()
    print(f"\nColumns ({len(columns)}):")
    for col in columns:
        print(f"  {col.name:35s}  group={col.column_group}")


if __name__ == "__main__":
    main()
