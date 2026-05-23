"""
Remove an event receiver by ID.

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
target_list = ctx.web.lists.get_by_title("Documents")
receivers = target_list.event_receivers.get().execute_query()
if receivers:
    target = receivers[0]
    receiver_id = target.properties.get("ReceiverId")
    if receiver_id:
        receiver = target_list.event_receivers.get_by_id(receiver_id)
        receiver.delete_object().execute_query()
        print(f"Removed event receiver: {receiver_id}")
