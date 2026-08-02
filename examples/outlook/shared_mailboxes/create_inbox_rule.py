"""
Create an inbox rule on a shared mailbox to auto-route incoming mail.

Example: messages matching "urgent" in the subject or body are marked as read
and forwarded to the shared mailbox owner. This is a common pattern for
support/customer-service mailboxes.

Requires delegated permission ``Mail.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailfolder-post-messagerules
"""

from office365.graph_client import GraphClient
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.recipient import Recipient
from tests import test_client_id, test_client_secret, test_shared_mailbox_upn, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

shared = client.users[test_shared_mailbox_upn]
inbox = shared.mail_folders["inbox"]

actions = MessageRuleActions(markAsRead=True)
actions.forwardTo.add(Recipient.from_email(test_username))

rule = inbox.message_rules.add(
    display_name="SDK example: mark read + forward urgent",
    sequence=1,
    actions=actions,
)
rule.conditions.bodyOrSubjectContains.add("urgent")
rule.update().execute_query()

print(f"Rule created on {test_shared_mailbox_upn}'s inbox: {rule.display_name}")
