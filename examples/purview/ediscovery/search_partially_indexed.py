"""
Run a compliance search for partially indexed items across SharePoint
and Exchange.

Partially indexed items (unsupported file types, encryption, or
indexing failures) are invisible to normal searches but can hold
relevant content for eDiscovery.

Requires delegated permission ``eDiscovery.ReadWrite.All``.

https://learn.microsoft.com/en-graph/api/resources/security-ediscoverysearch
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant

client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

case = client.security.cases.ediscovery_cases.add(
    displayName="Compliance scan — partially indexed items"
).execute_query()
if case.id is None:
    raise SystemExit("Failed to create eDiscovery case")

search = (
    client.security.cases.ediscovery_cases[case.id]
    .searches.add(
        displayName="Partially indexed items scan",
        content_query="*",
        data_source_scopes="allTenantMailboxes,allTenantSites",
    )
    .execute_query()
)

print(f"Search created: {search.id}")
print("Partially indexed items scan submitted (unsupported files, encryption, indexing failures).")
