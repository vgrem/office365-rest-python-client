"""
Upload a SharePoint Framework solution (.sppkg) to the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

ctx = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
app_file = ctx.web.tenant_app_catalog.app_from_path("./react-banner.sppkg", True).execute_query()
print(f"Uploaded: {app_file.name}")
