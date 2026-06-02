"""
List alerts for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
alerts = ctx.web.current_user.alerts.get().execute_query()
for a in alerts:
    print(f"  {a.title}  (ID: {a.id}, type: {a.alert_type})")
