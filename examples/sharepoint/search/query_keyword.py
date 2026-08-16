"""
Search for document files in tenant

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = ctx.search.query("IsDocument:1", row_limit=10).execute_query()
for row in result.value.PrimaryQueryResult.RelevantResults.Table.Rows:
    print("{0}".format(row.Cells["Path"]))
