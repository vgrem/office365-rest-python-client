"""
Import a taxonomy hierarchy from a JSON file into a Microsoft Graph term store.

JSON format mirrors the term store model:
  [group { name, sets: [ set { name, children: [ term { name, children: [] } ] } ] }]

Requires delegated permission ``TermStore.ReadWrite.All``.

Usage:
    python import_term_set.py
"""

import json
from pathlib import Path

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

data_file = (Path(__file__).parent / "../../data/regions.json").resolve()

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
store = client.sites.root.term_store


def _import_terms(terms, parent, depth=2):
    for t in terms:
        node = parent.get_or_add(t["name"]).execute_query()
        print(f"{'  ' * depth} Term: {t['name']}")
        for child in t.get("children", []):
            _import_terms([child], node.children, depth + 1)


with open(data_file) as f:
    for group_data in json.load(f):
        group = store.groups.get_or_add(group_data["name"]).execute_query()
        print(f"Group: {group_data['name']}")
        for set_data in group_data.get("sets", []):
            term_set = group.sets.get_or_add(set_data["name"]).execute_query()
            print(f"  Set: {set_data['name']}")
            _import_terms(set_data.get("children", []), term_set.children, 2)

print("Done")
