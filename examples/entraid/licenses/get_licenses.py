"""
Retrieve a list of licenseDetails objects for enterprise users.

https://learn.microsoft.com/en-us/graph/api/user-list-licensedetails?view=graph-rest-1.0

https://learn.microsoft.com/en-us/graph/api/resources/user

Requires delegated permission ``User.ReadWrite.All``.
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
result = client.me.license_details.get().execute_query()
for details in result:
    print(details)
