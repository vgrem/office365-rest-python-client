"""
Token acquisition via client secret using the built-in with_client_secret method.

The following options are supported:
   - Use the built-in GraphClient(tenant=tenant).with_client_secret(client_id, client_secret) method
   - Or provide a custom callback to the GraphClient constructor (see with_client_secret_custom.py)

https://learn.microsoft.com/en-us/graph/auth
https://learn.microsoft.com/en-us/entra/identity-platform/msal-authentication-flows#client-credentials
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
root_site = client.sites.root.get().execute_query()
print(root_site.web_url)
