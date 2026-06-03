"""
Create a change notification (webhook) subscription for new mail.

Microsoft Graph POSTs to the ``notification_url`` when new messages
arrive in the Inbox.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/subscription-post-subscriptions?view=graph-rest-1.0
"""

import datetime

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

expires = datetime.datetime.now() + datetime.timedelta(hours=120)
notification_url = "https://webhook.azurewebsites.net/api/send/myNotifyClient"
subscription = client.subscriptions.add(
    "created",
    notification_url,
    client.me.mail_folders["Inbox"].messages.resource_path,
    expires,
).execute_query()
print(subscription)
