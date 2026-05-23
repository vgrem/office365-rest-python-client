"""
List all apps available in the tenant app catalog.

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
apps = ctx.web.tenant_app_catalog.available_apps.get().execute_query()
for app in apps:
    print(f"  {app.title}  (ID: {app.id})")
print(f"Total: {len(apps)} app(s)")
