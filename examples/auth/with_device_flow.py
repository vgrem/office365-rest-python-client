"""
Device code flow authentication — ideal for CLI tools and headless
environments without a web browser.

The user authenticates by visiting a URL on another device (phone,
laptop) and entering the displayed code. No interactive browser is
needed on the machine running the script.

https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_tenant

client = GraphClient(tenant=test_tenant).with_device_flow(test_client_id)
me = client.me.get().execute_query()
print(f"Authenticated as: {me.user_principal_name}")
