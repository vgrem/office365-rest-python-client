"""
Retrieves SharePoint sites using search query.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

client = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

result = client.search.query("contentclass:STS_Site").execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    site_url = row.Cells["Path"]
    print(site_url)
