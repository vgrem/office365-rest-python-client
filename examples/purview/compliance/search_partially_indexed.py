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

search = (
    client.security.cases.ediscovery_cases[case.id]
    .searches.add(
        displayName="Partially indexed items scan",
        content_query="*",
        data_source_scopes="allTenantMailboxes,allTenantSites",
    )
    .execute_query()
)

estimate = search.estimate_statistics().execute_query()
print("Search:              Partially indexed items scan")
print(f"Status:              {estimate.status}")
print(f"Estimated hits:      {estimate.estimated_hits_count or 0}")
print(f"Partially indexed:   {estimate.estimated_partially_indexed_item_count or 0}")
print(f"Mailbox sources:     {estimate.estimated_mailbox_count or 0}")
print(f"Site sources:        {estimate.estimated_site_count or 0}")
