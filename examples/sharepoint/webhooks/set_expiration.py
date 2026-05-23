"""
Extend or update the expiration date of a webhook subscription.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/webhooks/overview/sharepoint-webhooks
"""

from datetime import datetime, timedelta

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = ctx.web.lists.get_by_title("Documents")
subscription = target_list.subscriptions.get().execute_query()[0]  # pick first subscription
new_expiry = datetime.utcnow() + timedelta(days=180)
subscription.expiration_datetime = new_expiry
subscription.update().execute_query()
print(f"Subscription {subscription.id} updated, expires: {subscription.expiration_datetime}")
