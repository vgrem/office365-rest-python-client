"""
List all webhook subscriptions on a SharePoint list.

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
subscriptions = target_list.subscriptions.get().execute_query()
for sub in subscriptions:
    print(f"ID: {sub.id}")
    print(f"  Notification URL: {sub.notification_url}")
    print(f"  Expires: {sub.expiration_datetime}")
    print(f"  App ID: {sub.application_id}")
