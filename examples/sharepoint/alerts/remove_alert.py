"""
Remove an alert by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(test_tenant, test_client_id, test_username, test_password)
target_list = ctx.web.lists.get_by_title("Documents")
alert_id = "your-alert-id"
alert = target_list.alerts.get_by_id(alert_id)
alert.delete_object().execute_query()
print("Alert removed")
