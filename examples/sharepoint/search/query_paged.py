"""
Paginate through large search results using start_row and row_limit.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
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
