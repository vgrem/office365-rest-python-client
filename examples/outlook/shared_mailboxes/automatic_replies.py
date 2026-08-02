"""
Read and configure automatic replies (out-of-office) on a shared mailbox.

Useful for shared HR/support mailboxes that should acknowledge incoming mail
during a period of absence.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/user-update-mailboxsettings
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_shared_mailbox_upn, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = client.users[test_shared_mailbox_upn]

settings = shared.select(["MailboxSettings"]).get().execute_query().mailbox_settings
print("Current automatic replies:", settings.automaticRepliesSetting.status or "disabled")

shared.enable_automatic_replies_setting(
    status="scheduled",
    scheduled_start_datetime=datetime.now(timezone.utc),
    scheduled_end_datetime=datetime.now(timezone.utc) + timedelta(days=1),
    internal_reply_message="We're away — a colleague will get back to you.",
).execute_query()
print("Automatic replies enabled for the shared mailbox.")
