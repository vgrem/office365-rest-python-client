"""
Add an alert on a list for the current user.

Alerts are created on the current user's alert collection, targeting
a specific list via the List property.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
target_list = ctx.web.lists.get_by_title("Documents")
alert = target_list.add_alert("My Alert").execute_query()
print("Alert created for list")
