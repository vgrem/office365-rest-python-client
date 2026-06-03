"""
Get and enable automatic replies (OOF) on the user's mailbox.

Sets an automatic reply to trigger during a specific time range with
an internal and external message.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailboxsettings-get?view=graph-rest-1.0
https://learn.microsoft.com/en-us/graph/api/user-update-mailboxsettings?view=graph-rest-1.0
"""

import datetime

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(
    test_client_id, test_username, test_password
)

# Read current automatic replies settings
settings = client.me.mailbox_settings.automatic_replies_setting.get().execute_query()
print(f"Status: {settings.status}")

# Enable scheduled automatic replies
start_time = datetime.datetime.utcnow()
end_time = start_time + datetime.timedelta(days=7)

client.me.mailbox_settings.automatic_replies_setting.set(
    status="scheduled",
    scheduled_start_date_time=start_time,
    scheduled_end_date_time=end_time,
    internal_reply_message="I'm out of the office this week.",
    external_reply_message="I'm out of the office. I'll respond when I return.",
).execute_query()
print("Automatic replies enabled for 7 days")
