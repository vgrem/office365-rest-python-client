"""
Analyze sensitivity label usage — list labels with priority and description.

Requires delegated permission ``InformationProtectionPolicy.Read.All``
and Global Administrator or Compliance Administrator role.

https://learn.microsoft.com/en-us/graph/api/resources/sensitivitylabel
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant, scopes=["https://graph.microsoft.com/InformationProtectionPolicy.Read.All"])
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Compliance Administrator")
)

labels = client.security.data_security_and_governance.sensitivity_labels.get().execute_query()
print(f"Sensitivity labels ({len(labels)}):\n")
print(f"{'Label':35s} {'Priority':>10s} {'Description'}")
print("-" * 85)
for label in labels:
    print(f"{label.display_name[:33]:35s} {label.priority:>10d} {label.description}")
