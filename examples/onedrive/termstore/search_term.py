"""
Search for a term by label across all sets in the term store.

Finds which group and set a term belongs to — useful for
locating where a specific tag is used in the taxonomy.

Requires delegated permission Sites.ReadWrite.All.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_root_site_url, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    store = client.sites.get_by_url(test_root_site_url).term_store

    search_label = "Canada"
    terms = store.search_term(search_label).execute_query()
    for t in terms:
        print(f"Found: {search_label}")
        print(f"  Term:  {t.display_name}: {t.id}")


if __name__ == "__main__":
    main()
