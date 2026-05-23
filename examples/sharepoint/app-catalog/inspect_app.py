"""
Get metadata about a specific app in the tenant app catalog.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_site_url, test_client_id, test_tenant, test_username, test_password

ctx = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
app = ctx.web.tenant_app_catalog.available_apps.get_by_title("Starter Kit - Banner").execute_query()
print(f"Title: {app.title}")
print(f"Version: {app.app_catalog_version}")
print(f"Can upgrade: {app.can_upgrade}")
print(f"Is client-side: {app.is_client_side_solution}")
print(f"AAD permissions: {app.aad_permissions}")
