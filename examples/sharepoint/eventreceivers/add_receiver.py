"""
Add a remote event receiver to a SharePoint list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-event-receiver
"""

from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.eventreceivers.definition import EventReceiverDefinition
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = ctx.web.lists.get_by_title("Documents")

receiver = EventReceiverDefinition(ctx)
receiver.set_property("ReceiverName", "RemoteItemAdded")
receiver.set_property("ReceiverUrl", "https://your-app.azurewebsites.net/webhook")
receiver.set_property("EventType", 2)  # ItemAdded
receiver.set_property("Synchronization", 1)  # Asynchronous
receiver.set_property("SequenceNumber", 1000)
qry = CreateEntityQuery(target_list.event_receivers, receiver)
ctx.add_query(qry)
ctx.execute_query()
print(f"Event receiver added: {receiver.properties.get('ReceiverId')}")
