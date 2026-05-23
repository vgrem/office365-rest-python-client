"""
Remove a webhook subscription from a SharePoint list.

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

# Option 1 — delete by subscription entity
subscription = target_list.subscriptions.get().execute_query()[0]
subscription.delete_object().execute_query()
print(f"Subscription {subscription.id} deleted")

# Option 2 — remove by ID directly
# target_list.subscriptions.remove("subscription-id-here").execute_query()
