"""
List Azure AD directory audit logs via Microsoft Graph.

https://learn.microsoft.com/en-us/graph/api/directoryaudit-list
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
audits = client.audit_logs.directory_audits.top(10).get().execute_query()
for a in audits:
    print(f"{a.activity_datetime}: {a.activity_display_name} ({a.category})")
