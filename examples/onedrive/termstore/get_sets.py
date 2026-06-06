"""
Get term sets in a Group

https://learn.microsoft.com/en-us/graph/api/resources/drive

Requires delegated permission ``TermStore.Read.All``.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
term_store = client.sites.root.term_store
sets = term_store.groups.get_by_name("Regions").sets.get().execute_query()
# term_set = group.sets.get_by_name("Locations").get().execute_query()
for ts in sets:
    print(ts)
