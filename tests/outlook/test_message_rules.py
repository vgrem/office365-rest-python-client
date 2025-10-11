from office365.outlook.mail.importance import Importance
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.rule import MessageRule
from office365.outlook.mail.recipient import Recipient
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestMessageRules(GraphTestCase):
    target_message_rule: MessageRule = None

    @requires_delegated_permission("MailboxSettings.ReadWrite")
    def test1_create_rule(self):
        actions = MessageRuleActions(
            forward_to=[Recipient.from_email("AlexW@contoso.com")],
            stop_processing_rules=True,
            mark_importance=Importance.normal,
        )
        result = self.client.me.mail_folders["inbox"].message_rules.add("From partner", 2, actions).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_message_rule = result

    @requires_delegated_permission("MailboxSettings.Read", "MailboxSettings.ReadWrite")
    def test2_list_rules(self):
        message_rules = self.client.me.mail_folders["inbox"].message_rules.get().execute_query()
        self.assertIsNotNone(message_rules.resource_path)

    @requires_delegated_permission("MailboxSettings.ReadWrite")
    def test3_update_rule(self):
        rule = self.__class__.target_message_rule
        rule.actions.markImportance = Importance.high
        rule.update().execute_query()

    @requires_delegated_permission("MailboxSettings.Read", "MailboxSettings.ReadWrite")
    def test4_get_rule(self):
        result = self.__class__.target_message_rule.get().execute_query()
        self.assertEqual(result.actions.markImportance, "high")

    @requires_delegated_permission("MailboxSettings.ReadWrite")
    def test5_delete_rule(self):
        rule = self.__class__.target_message_rule
        rule.delete_object().execute_query()
