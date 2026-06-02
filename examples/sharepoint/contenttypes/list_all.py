"""Demonstrates how to enumerate all content types on a SharePoint site.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
cts = ctx.web.content_types.get().execute_query()
for ct in cts:
    print(f"  {ct.name}  (ID: {ct.id})")
print(f"Total: {len(cts)} content types")