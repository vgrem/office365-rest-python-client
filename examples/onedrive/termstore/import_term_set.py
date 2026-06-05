"""
Import a region hierarchy (countries -> districts -> cities) from a JSON file
into a Microsoft Graph term store under the root site.

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
group = store.groups.get_or_add("Regions").execute_query()
term_set = group.sets.add("Countries").execute_query()

with open(data_file) as f:
    for country in json.load(f):
        term = term_set.children.add(country["name"]).execute_query()
        for district in country.get("districts", []):
            child = term.children.add(district["name"]).execute_query()
            for city in district.get("cities", []):
                child.children.add(city).execute_query()

print("Imported countries with regions and cities.")
