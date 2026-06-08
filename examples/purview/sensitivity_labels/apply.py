"""
Sensitivity labels: apply labels to files, check labels on
Microsoft 365 groups, and audit label usage.

Essential for information protection governance.

Requires delegated permission ``InformationProtectionPolicy.Read.All``,
``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/informationprotectionpolicy-list-labels
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. List sensitivity labels
labels = client.security.information_protection.sensitivity_labels.top(20).get().execute_query()
print(f"Sensitivity labels ({len(labels)}):")
for label in labels:
    print(f"  {label.display_name:30s}  id: {label.id}")
