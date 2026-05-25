"""
List Azure AD sign-in logs via Microsoft Graph.

https://learn.microsoft.com/en-us/graph/api/signin-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
signins = client.audit_logs.signins.top(10).get().execute_query()
for s in signins:
    print(f"{s.created_datetime}: {s.user_display_name} ({s.status})")
