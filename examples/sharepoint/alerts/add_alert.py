"""
Add an alert on a list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.alerts.creation_information import AlertCreationInformation
from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
target_list = ctx.web.lists.get_by_title("Documents")
params = AlertCreationInformation(
    Title="My Alert",
    AlertType=1,  # list alert
    EventTypeBitmask=1,  # item added
)
alert = target_list.alerts.add(params).execute_query()
print(f"Alert created: {alert.title}  (ID: {alert.id})")
