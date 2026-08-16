"""
Faceted search — request refiners and drill down with refinement filters.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

# Step 1 — query with refiners to get category counts
result = ctx.search.query(
    query_text="IsDocument:1",
    refiners=["Author", "ContentType", "FileExtension"],
    row_limit=10,
).execute_query()

print("=== Refiners ===")
refiners = result.value.PrimaryQueryResult.RefinementResults.Refiners
for refiner in refiners:
    print(f"  {refiner.Name}:")
    for entry in refiner.Entries:
        print(f"    {entry.RefinementName} ({entry.RefinementCount}) — token: {entry.RefinementToken}")

# Step 2 — drill down with a refinement filter
if refiners and refiners[0].Entries:
    token = refiners[0].Entries[0].RefinementToken
    result = ctx.search.query(
        query_text="IsDocument:1",
        refinement_filters=[token],
        row_limit=10,
    ).execute_query()
    print(f"\n=== Filtered by {refiners[0].Entries[0].RefinementName} ===")
    results = result.value.PrimaryQueryResult.RelevantResults
    for row in results.Table.Rows:
        print(row.Cells["Path"])
