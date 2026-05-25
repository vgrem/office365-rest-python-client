"""
Set site collection properties (title, description, etc.).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
web = ctx.web.get().execute_query()
web.set_property("Title", "Updated Title")
web.update().execute_query()
print(f"Site title updated: {web.title}")
