"""
Demonstrates how to sort search results using the SharePoint Search REST service.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.search.query.sort.sort import Sort
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = ctx.search.query(
    query_text="IsDocument:1",
    sort_list=[Sort(Property="LastModifiedTime", Direction=1)],
    select_properties=["Path", "LastModifiedTime"],
    row_limit=20,
).execute_query()

results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    print(row.Cells["Path"], row.Cells["LastModifiedTime"])
