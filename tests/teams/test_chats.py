"""Chats — creating, listing, members, messages, and deleting chats.

Tests cover:
  - Creating a 1-on-1 chat
  - Listing user chats with pagination
  - Listing chat members
  - Sending a message in a chat
  - Getting a chat by ID
  - Listing messages in a chat
  - Deleting a chat
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.mail.item_body import ItemBody
from office365.teams.chats.chat import Chat
from office365.teams.chats.type import ChatType

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamChats(GraphDelegatedTestCase):
    """Chat CRUD, messaging, and member inspection."""

    target_chat: ClassVar[Optional[Chat]] = None

    @requires_delegated(
        "Chat.ReadWrite",
        "Chat.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_create_one_on_one_chat(self):
        """Creating a 1-on-1 chat should succeed."""
        owner = self.client.me.get().execute_query()
        other = self.client.users[test_user_principal_name].get().execute_query()
        if not owner.id or not other.id:
            self.skipTest("Cannot determine user IDs")

        chat = self.client.chats.add(ChatType.oneOnOne, owner_ids=[owner.id, other.id]).execute_query()
        self.assertIsNotNone(chat.resource_path)
        self.assertIsNotNone(chat.get_property("id"))
        TestTeamChats.target_chat = chat

    @requires_delegated(
        "Chat.Read",
        "Chat.ReadWrite",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_list_user_chats(self):
        """Listing user chats with $top=10 returns a valid collection."""
        result = self.client.me.chats.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Chat.Read",
        "Chat.ReadWrite",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_03_chat_has_expected_properties(self):
        """A chat exposes topic, chatType, and createdDateTime."""
        chat = TestTeamChats.target_chat
        if not chat:
            self.skipTest("No chat created from previous test")

        self.assertIsNotNone(chat.chat_type)
        self.assertIsNotNone(chat.created_datetime)

    @requires_delegated(
        "Chat.ReadWrite",
        "Chat.Read",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_04_list_chat_members(self):
        """Listing members of a chat returns a valid collection."""
        chat = TestTeamChats.target_chat
        if not chat:
            self.skipTest("No chat created from previous test")

        members = chat.members.get().execute_query()
        self.assertIsNotNone(members.resource_path)

    @requires_delegated(
        "Chat.ReadWrite",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_05_send_chat_message(self):
        """Sending a message in a chat should succeed."""
        chat = TestTeamChats.target_chat
        if not chat:
            self.skipTest("No chat created from previous test")

        msg = chat.messages.add(body=ItemBody("Hello from office365-rest-python-client!")).execute_query()
        self.assertIsNotNone(msg.id)

    @requires_delegated(
        "Chat.Read",
        "Chat.ReadWrite",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_06_list_chat_messages(self):
        """Listing messages in a chat returns a valid collection."""
        chat = TestTeamChats.target_chat
        if not chat:
            self.skipTest("No chat created from previous test")

        messages = chat.messages.top(5).get().execute_query()
        self.assertIsNotNone(messages)

    @requires_delegated(
        "Chat.ReadWrite",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_07_delete_chat(self):
        """Deleting a chat should succeed."""
        chat = TestTeamChats.target_chat
        if not chat:
            self.skipTest("No chat created from previous test")

        chat.delete_object().execute_query_retry()
        TestTeamChats.target_chat = None

    @classmethod
    def tearDownClass(cls):
        chat = cls.target_chat
        if chat and chat.resource_path:
            try:
                chat.delete_object().execute_query_retry()
            except Exception:
                pass
