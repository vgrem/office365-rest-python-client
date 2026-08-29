"""
Export the term store hierarchy as nested JSON, then re-import it.

Demonstrates the symmetric pair on StoreManager: ``to_json()`` walks
groups -> sets -> terms -> children into a nested tree, and ``from_json()``
restores it. CSV flattens hierarchical data; JSON preserves it.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    manager = client.sites.root.term_store

    # Export: nested tree [{name, sets: [{name, children: [...]}]}]
    result = manager.to_json().execute_query()
    tree = result.value
    print(f"Exported {len(tree)} group(s): {[g['name'] for g in tree]}")

    # The round-trip: from_json restores the same hierarchy (queued creates)
    manager.from_json(tree)
    client.execute_query()
    print("Re-imported the hierarchy (creates queued and submitted).")


if __name__ == "__main__":
    main()
