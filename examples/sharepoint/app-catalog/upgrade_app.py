"""
Upgrade an app to a newer version available in the tenant app catalog.

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
app = ctx.web.tenant_app_catalog.available_apps.get_by_title("Starter Kit - Banner").execute_query()
if app.can_upgrade:
    app.deploy(skip_feature_deployment=False).execute_query()
    app.install().execute_query()
    print(f"Upgraded: {app.title}")
else:
    print(f"No upgrade available for {app.title}")
