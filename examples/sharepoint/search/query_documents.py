"""
Search for document files in a SharePoint tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

result = ctx.search.post_query(query_text="IsDocument:1").execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    file_url = row.Cells["Path"]
    print(file_url)
