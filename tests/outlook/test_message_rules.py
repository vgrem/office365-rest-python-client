from typing import Optional

from office365.outlook.mail.importance import Importance
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.rule import MessageRule
from office365.outlook.mail.recipient import Recipient

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestMessageRules(GraphDelegatedTestCase):
    target_message_rule: Optional[MessageRule] = None

    @requires_delegated("MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test1_create_rule(self):
        actions = MessageRuleActions(
            forward_to=[Recipient.from_email("AlexW@contoso.com")],
            stop_processing_rules=True,
            mark_importance=Importance.normal,
        )
        result = self.client.me.mail_folders["inbox"].message_rules.add("From partner", 2, actions).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestMessageRules.target_message_rule = result

    @requires_delegated(
        "MailboxSettings.Read", "MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"]
    )
    def test2_list_rules(self):
        message_rules = self.client.me.mail_folders["inbox"].message_rules.get().execute_query()
        self.assertIsNotNone(message_rules.resource_path)

    @requires_delegated("MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test3_update_rule(self):
        assert TestMessageRules.target_message_rule is not None
        rule = TestMessageRules.target_message_rule
        rule.actions.markImportance = Importance.high
        rule.update().execute_query()

    @requires_delegated(
        "MailboxSettings.Read", "MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"]
    )
    def test4_get_rule(self):
        assert TestMessageRules.target_message_rule is not None
        result = TestMessageRules.target_message_rule.get().execute_query()
        self.assertEqual(result.actions.markImportance, "high")

    @requires_delegated("MailboxSettings.ReadWrite", or_roles=["Exchange Administrator", "Global Administrator"])
    def test5_delete_rule(self):
        assert TestMessageRules.target_message_rule is not None
        rule = TestMessageRules.target_message_rule
        rule.delete_object().execute_query()
