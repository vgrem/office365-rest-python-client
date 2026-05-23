"""
Search with property filters — author, date range, and custom managed properties.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
# KQL syntax: Author:"John Smith" AND LastModifiedTime>2024-01-01
result = ctx.search.query(
    query_text='Author:"John Smith" LastModifiedTime>2024-01-01',
    select_properties=["Path", "Title", "Author", "LastModifiedTime"],
    row_limit=20,
).execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    print(row.Cells["Path"], row.Cells.get("Author", ""), row.Cells.get("LastModifiedTime", ""))
