"""Inbox rules — creating, listing, updating, and deleting message rules.

Tests cover:
  - Creating a forwarding rule with actions (forwardTo, markImportance)
  - Listing rules on the inbox
  - Updating rule action properties (markImportance)
  - Getting a specific rule by ID
  - Deleting a rule and verifying removal
  - Rule property assertions (displayName, priority, actions)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.mail.importance import Importance
from office365.outlook.mail.messages.rules.actions import MessageRuleActions
from office365.outlook.mail.messages.rules.rule import MessageRule
from office365.outlook.mail.recipient import Recipient
from office365.runtime.client_value_collection import ClientValueCollection

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestMessageRules(GraphDelegatedTestCase):
    """Inbox message rule CRUD and lifecycle."""

    target_rule: ClassVar[Optional[MessageRule]] = None

    @requires_delegated(
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_forwarding_rule(self):
        """Creating a rule that forwards mail with importance should succeed."""
        actions = MessageRuleActions(
            forwardTo=ClientValueCollection(Recipient, [Recipient.from_email("AlexW@contoso.com")]),
            stopProcessingRules=True,
            markImportance=Importance.normal,
        )
        result = self.client.me.mail_folders["inbox"].message_rules.add(
            "SDK Test Rule", 2, actions
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), "SDK Test Rule")
        self.assertIsNotNone(result.get_property("priority"))
        TestMessageRules.target_rule = result

    @requires_delegated(
        "MailboxSettings.Read", "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_list_rules(self):
        """Listing inbox rules returns a valid collection."""
        rules = self.client.me.mail_folders["inbox"].message_rules.get().execute_query()
        self.assertIsNotNone(rules.resource_path)

    @requires_delegated(
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_update_rule_importance(self):
        """Updating a rule's markImportance to high should persist."""
        rule = TestMessageRules.target_rule
        if not rule:
            self.skipTest("No rule created from previous test")

        rule.actions.markImportance = Importance.high
        rule.update().execute_query()

    @requires_delegated(
        "MailboxSettings.Read", "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_get_rule_by_id(self):
        """Getting a rule by ID returns the rule with updated properties."""
        rule = TestMessageRules.target_rule
        if not rule:
            self.skipTest("No rule created from previous test")

        result = rule.get().execute_query()
        self.assertEqual(result.get_property("actions")["markImportance"], "high")
        self.assertEqual(result.get_property("displayName"), "SDK Test Rule")

    @requires_delegated(
        "MailboxSettings.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_delete_rule(self):
        """Deleting a rule should succeed."""
        rule = TestMessageRules.target_rule
        if not rule:
            self.skipTest("No rule created from previous test")

        rule.delete_object().execute_query()
        TestMessageRules.target_rule = None

    @classmethod
    def tearDownClass(cls):
        rule = cls.target_rule
        if rule and rule.resource_path:
            try:
                rule.delete_object().execute_query()
            except Exception:
                pass
