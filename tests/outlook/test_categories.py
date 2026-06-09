"""Outlook categories — master categories CRUD and assignment.

Tests cover:
  - Creating a master category with displayName and color
  - Listing master categories
  - Assigning a category to a message
  - Category property assertions
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.mail.messages.message import Message

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookCategories(GraphDelegatedTestCase):
    """Master category lifecycle and message assignment."""

    target_msg: ClassVar[Optional[Message]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        msg = cls.client.me.messages.add(subject="Category Test", body="Testing categories.").execute_query()
        cls.target_msg = msg

    @classmethod
    def tearDownClass(cls):
        msg = cls.target_msg
        if msg and msg.resource_path:
            try:
                msg.delete_object().execute_query()
            except Exception:
                pass

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_master_category(self):
        """Creating a master category with a displayName and color should succeed."""
        name = create_unique_name("SDK Test Category")
        result = self.client.me.outlook.master_categories.add(display_name=name, color="preset5").execute_query()
        self.assertIsNotNone(result.id)
        self.assertEqual(result.display_name, name)
        self.assertEqual(result.color, "preset5")

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_list_master_categories(self):
        """Listing master categories returns a valid collection."""
        result = self.client.me.outlook.master_categories.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        if len(result) > 0:
            self.assertIsNotNone(result[0].display_name)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_assign_category_to_message(self):
        """Assigning a category to a message via the categories property should succeed."""
        msg = TestOutlookCategories.target_msg
        if not msg:
            self.skipTest("No target message available")

        msg.set_property("categories", ["Urgent"]).update().execute_query()
        updated = self.client.me.messages[msg.id].get().execute_query()
        cats = updated.get_property("categories") or []
        self.assertIn("Urgent", cats)
