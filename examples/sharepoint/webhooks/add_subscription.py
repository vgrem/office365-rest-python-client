"""
Subscribe to list change notifications via a SharePoint webhook.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = ctx.web.lists.get_by_title("Documents")
subscription = target_list.subscriptions.add("https://your-app.azurewebsites.net/webhook/notifications").execute_query()
print(f"Subscription created: {subscription.id}")
print(f"Notification URL: {subscription.notification_url}")
print(f"Expires: {subscription.expiration_datetime}")
