"""
Import a taxonomy hierarchy into a Microsoft Graph term store from JSON or CSV.

JSON format mirrors the term store model:
  [group { name, sets: [ set { name, children: [ term { name, children: [] } ] } ] }]

CSV format:
  group,set,term,parent_term
  Rows are processed in order — parents must appear before children.

Requires delegated permission TermStore.ReadWrite.All.
"""

from pathlib import Path

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def _import_terms(collection, terms):
    for t in terms:
        node = collection.get_or_add(t["name"])
        _import_terms(node.children, t.get("children", []))


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    json_path = Path("../../data/regions.json")
    if not json_path.exists():
        raise FileNotFoundError(json_path)

    store = client.sites.root.term_store
    store.import_from_json(json_path).execute_query()
    print(f"Imported from {json_path}")


if __name__ == "__main__":
    main()
