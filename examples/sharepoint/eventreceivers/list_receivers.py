"""
List all event receivers on a SharePoint list or web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# List-scoped event receivers
target_list = ctx.web.lists.get_by_title("Documents")
receivers = target_list.event_receivers.get().execute_query()
print(f"=== Event receivers on 'Documents' ({len(receivers)}) ===")
for r in receivers:
    print(
        f"  {r.properties.get('ReceiverName', '')}  "
        f"(EventType: {r.properties.get('EventType', '')}, "
        f"ReceiverId: {r.properties.get('ReceiverId', '')})"
    )
