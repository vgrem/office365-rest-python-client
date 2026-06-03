"""
List retention labels in Microsoft Purview.

Retention labels define how long content is kept and what action to take
after the retention period.

Requires delegated permission ``RecordsManagement.Read.All`` or
``RecordsManagement.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/security-list-retentionlabels?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

labels = client.security.labels.retention_labels.get().execute_query()
for label in labels:
    name = label.display_name or label.name or "(unnamed)"
    print(f"  {name}")
