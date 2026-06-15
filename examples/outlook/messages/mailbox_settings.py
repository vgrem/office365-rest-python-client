"""
Get and enable automatic replies (Out of Office).

Shows how to read and update mailbox settings for automatic
replies.

Requires delegated permission ``Mail.ReadWrite`` or
``MailboxSettings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-update-mailboxsettings
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# Read current mailbox settings
me = client.me.select(["MailboxSettings"]).get().execute_query()
print(f"Current automatic replies: {me.mailbox_settings.automaticRepliesSetting}")

start = datetime.now()
end = start + timedelta(days=5)
me.enable_automatic_replies_setting(
    status="scheduled",
    scheduled_start_datetime=start,
    scheduled_end_datetime=end,
    internal_reply_message="I'm out of the office this week.",
    external_reply_message="I'm out of the office. Please contact my manager.",
).execute_query()

print("Automatic replies enabled")
