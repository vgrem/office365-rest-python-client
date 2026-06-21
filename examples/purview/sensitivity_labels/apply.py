"""
List sensitivity labels available in the tenant.

Requires delegated permission ``InformationProtectionPolicy.Read.All``
and Global Administrator or Compliance Administrator role.

https://learn.microsoft.com/en-us/graph/api/informationprotectionpolicy-list-labels
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant, scopes=["https://graph.microsoft.com/InformationProtectionPolicy.Read.All"])
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Compliance Administrator")
)

labels = client.security.data_security_and_governance.sensitivity_labels.top(20).get().execute_query()
print(f"Sensitivity labels ({len(labels)}):")
for label in labels:
    print(f"  {label.display_name:30s}  id: {label.id}")
