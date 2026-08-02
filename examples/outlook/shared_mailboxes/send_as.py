"""
Send an email as a shared mailbox (the From address is the shared mailbox).

The signed-in identity must have Send-As rights granted on the shared
mailbox — an Exchange Online admin action. The message is sent via the
shared mailbox's own sendMail endpoint, so the From header is the shared
mailbox address rather than the sender's.

Requires delegated permission ``Mail.Send`` (or app permission ``Mail.Send``).

https://learn.microsoft.com/en-us/graph/api/user-sendmail
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_shared_mailbox_upn, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = client.users[test_shared_mailbox_upn]
shared.send_mail(
    subject="Sent from a shared mailbox",
    body="This message was sent via office365-rest-python-client.",
    to_recipients=[test_username],
).execute_query()
print(f"Email sent from {test_shared_mailbox_upn} to {test_username}.")
