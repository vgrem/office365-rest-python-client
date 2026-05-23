"""
Search documents by content type using the ContentType managed property.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.search.query.sort.sort import Sort
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = ctx.search.query(
    query_text="ContentType:document",
    sort_list=[Sort(Property="LastModifiedTime", Direction=1)],
    select_properties=["Path", "Title", "LastModifiedTime", "ContentType"],
    row_limit=20,
).execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    print(row.Cells["Path"], row.Cells.get("Title", ""), row.Cells.get("ContentType", ""))
