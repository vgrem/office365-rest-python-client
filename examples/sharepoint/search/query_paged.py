"""
Paginate through large search results using start_row and row_limit.

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
page_size = 50
start_row = 0
total = 0
while True:
    result = ctx.search.query(
        query_text="IsDocument:1",
        start_row=start_row,
        row_limit=page_size,
        select_properties=["Path", "Title"],
    ).execute_query()
    relevant = result.value.PrimaryQueryResult.RelevantResults
    rows = relevant.Table.Rows
    if not rows:
        break
    for row in rows:
        total += 1
        print(f"[{total}] {row.Cells['Path']}")
    start_row += len(rows)
print(f"Total results fetched: {total}")
