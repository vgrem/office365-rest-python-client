"""
Search for a term by label across all sets in the term store.

Finds which group and set a term belongs to — useful for locating where a
specific tag is used in the taxonomy.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/termstore-store-search
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, root_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Search the term store by term label")
    parser.add_argument("--label", required=True, help="term label to search for, e.g. 'Canada'")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    store = client.sites.get_by_url(root_site_url).term_store

    terms = store.search_term(args.label).execute_query()
    print(f"Matches for '{args.label}' ({len(terms)}):")
    for t in terms:
        print(f"  {t.display_name}  (id: {t.id})")


if __name__ == "__main__":
    main()
