"""
Search with property filters — author, date range, and custom managed properties.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
# KQL syntax: Author:"John Smith" AND LastModifiedTime>2024-01-01
# post_query is used instead of query to avoid URL encoding issues
# with special KQL characters (quotes, >) in the GET request path
result = ctx.search.post_query(
    query_text='Author:"John Smith" LastModifiedTime>2024-01-01',
    select_properties=["Path", "Title", "Author", "LastModifiedTime"],
    row_limit=20,
).execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    print(row.Cells["Path"], row.Cells.get("Author", ""), row.Cells.get("LastModifiedTime", ""))
