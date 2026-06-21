"""
Remove an alert by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

alert_id = "your-alert-id"
alert = ctx.web.current_user.alerts.get_by_id(alert_id)
alert.delete_object().execute_query()
print("Alert removed")
