"""
Create an inbox rule and manage message categories.

Combines two related patterns — rules for automated message handling
and categories for visual organization.

Requires delegated permission ``Mail.ReadWrite`` and
``MailboxSettings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/mailfolder-post-messagerules
https://learn.microsoft.com/en-us/graph/api/outlookuser-post-mastercategories
"""

from office365.graph_client import GraphClient
from office365.outlook.mail.importance import Importance
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value_collection import ClientValueCollection
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# 1. Create a master category
category = client.me.outlook.master_categories.add(display_name="Urgent", color="preset5").execute_query()
print(f"Category created: {category.display_name}")

# 2. Create an inbox rule: mark as Urgent when from specific sender
actions = MessageRuleActions(
    forwardTo=ClientValueCollection(Recipient, [Recipient.from_email("fannyd@contoso.onmicrosoft.com")]),
    stopProcessingRules=True,
    markImportance=Importance.high,
)
rule = client.me.mail_folders["inbox"].message_rules.add("SDK Test Rule", 2, actions).execute_query()
print(f"Rule created: {rule.display_name} (priority: {rule.priority})")
