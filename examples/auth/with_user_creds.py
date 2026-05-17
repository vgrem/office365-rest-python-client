"""
Username/Password (Resource Owner Password Credentials) flow using the built-in method.

Uses GraphClient.with_username_and_password for direct token acquisition.

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth-ropc
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)
me = client.me.get().execute_query()
print(me)
