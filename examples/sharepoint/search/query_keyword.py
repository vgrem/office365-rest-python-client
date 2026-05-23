"""
Search for document files in tenant

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
result = ctx.search.query("IsDocument:1", row_limit=10).execute_query()
for row in result.value.PrimaryQueryResult.RelevantResults.Table.Rows:
    print("{0}".format(row.Cells["Path"]))
