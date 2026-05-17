"""
Get a collection of sites.

https://learn.microsoft.com/en-us/onedrive/developer/rest-api/api/site_list_subsites?view=odsp-graph-online
https://learn.microsoft.com/en-us/graph/api/resources/drive
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
sites = client.sites.top(100).get().execute_query()
for site in sites:
    print(f"Site url: {site.web_url}")
