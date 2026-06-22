"""
Search for a term by label across all sets in the term store.

Finds which group and set a term belongs to — useful for
locating where a specific tag is used in the taxonomy.

Requires delegated permission Sites.ReadWrite.All.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, root_site_url, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    store = client.sites.get_by_url(root_site_url).term_store

    search_label = "Canada"
    terms = store.search_term(search_label).execute_query()
    for t in terms:
        print(f"Found: {search_label}")
        print(f"  Term:  {t.display_name}: {t.id}")


if __name__ == "__main__":
    main()
