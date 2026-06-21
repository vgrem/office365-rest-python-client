"""
List all retention labels in the tenant.

Requires delegated permission ``RecordsManagement.Read.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-retentionlabels
"""

from office365.graph_client import GraphClient
from tests.settings import admin_username, client_id, tenant

client = (
    GraphClient(tenant=tenant)
    .with_token_interactive(client_id, admin_username)
    .require_role("Global Administrator", "Compliance Administrator")
)

labels = client.security.labels.retention_labels.get().execute_query()
print(f"Retention labels ({len(labels)}):")
for label in labels:
    print(f"  {label.display_name:40s}  trigger={label.retention_trigger}  in_use={label.is_in_use}")
