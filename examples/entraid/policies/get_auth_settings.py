"""
Retrieves the tenant's authorization policy settings.

https://learn.microsoft.com/en-us/graph/api/authorizationpolicy-get
"""

from pprint import pprint

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

result = client.policies.authorization_policy.get().execute_query()
pprint(result.to_json())
