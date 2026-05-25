"""
Get audit settings for a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/audit
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
audit = ctx.site.audit.get().execute_query()
print(f"Allow designer: {audit.allow_designer}")
