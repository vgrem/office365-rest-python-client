"""
Uninstall an app from a target site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/alm-api-for-spfx-add-ins
"""

from office365.sharepoint.client_context import ClientContext
from tests import (
    test_admin_site_url,
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)

admin = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
app = admin.web.tenant_app_catalog.available_apps.get_by_title("Starter Kit - Banner").execute_query()
app.uninstall().execute_query()
print(f"Uninstalled: {app.title} from {test_team_site_url}")
