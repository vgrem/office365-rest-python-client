"""
Check if a delegated permission (OAuth scope) is granted to your app.

https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph
"""

from office365.directory.permissions.guard import has_delegated_permission
from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

scope = input("Permission scope: ")

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

if has_delegated_permission(client, scope, test_client_id):
    print(f"✅ Permission '{scope}' is granted.")
else:
    print(f"❌ Permission '{scope}' is not granted.")
