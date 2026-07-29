"""
Search SharePoint sites where the current user is a member.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
result = ctx.search.query("contentclass:STS_Site").execute_query()
results = result.value.PrimaryQueryResult.RelevantResults
for row in results.Table.Rows:
    print(row.Cells["Path"])  # prints site url
