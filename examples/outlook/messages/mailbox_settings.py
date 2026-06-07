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
settings = client.me.mailbox_settings.get().execute_query()
print(f"Current automatic replies: {settings.automatic_replies_status}")

# Enable scheduled automatic replies
settings.set_property(
    "automaticRepliesSetting",
    {
        "status": "scheduled",
        "scheduledStartDateTime": {
            "dateTime": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "timeZone": "UTC",
        },
        "scheduledEndDateTime": {
            "dateTime": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "timeZone": "UTC",
        },
        "internalReplyMessage": "I'm out of the office this week.",
        "externalReplyMessage": "I'm out of the office. Please contact my manager.",
    },
).update().execute_query()
print("Automatic replies enabled")
