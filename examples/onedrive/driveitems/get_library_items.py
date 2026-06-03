"""
Enumerate items in a list

https://learn.microsoft.com/en-us/graph/api/listitem-list?view=graph-rest-1.0
https://learn.microsoft.com/en-us/graph/api/resources/drive

Requires delegated permission ``Sites.Read.All``.
"""


from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
site = client.sites.get_by_url(test_team_site_url)
items = site.lists["Documents"].items.get().execute_query()
for item in items:
    print(item.web_url)
