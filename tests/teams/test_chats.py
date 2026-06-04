from typing import Optional

from office365.outlook.mail.item_body import ItemBody
from office365.teams.chats.chat import Chat
from office365.teams.chats.type import ChatType

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamChats(GraphDelegatedTestCase):
    """Tests for team Chats"""

    target_chat: Optional[Chat] = None

    @requires_delegated("Chat.ReadWrite", "Chat.Read", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test1_create(self):
        """Test creating a chat"""
        owner = self.client.me.get().execute_query()
        another_owner = self.client.users[test_user_principal_name].get().execute_query()
        assert owner.id is not None
        assert another_owner.id is not None

        new_chat = self.client.chats.add(ChatType.oneOnOne, owner_ids=[owner.id, another_owner.id]).execute_query()
        self.assertIsNotNone(new_chat.resource_path)
        TestTeamChats.target_chat = new_chat

    @requires_delegated("Chat.Read", "Chat.ReadWrite", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test2_list_user_chats(self):
        """Test listing user chats"""
        result = self.client.me.chats.get().top(10).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 0)

    @requires_delegated("Chat.ReadWrite", "Chat.Read", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test3_list_members(self):
        """List members of the chat."""
        assert TestTeamChats.target_chat is not None
        members = TestTeamChats.target_chat.members.get().execute_query()
        self.assertIsNotNone(members.resource_path)

    @requires_delegated("Chat.ReadWrite", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test4_send_message(self):
        """Send a message in the chat."""
        assert TestTeamChats.target_chat is not None
        msg = TestTeamChats.target_chat.messages.add(
            body=ItemBody("Hello from office365-rest-python-client!")
        ).execute_query()
        self.assertIsNotNone(msg.id)

    @requires_delegated("Chat.Read", "Chat.ReadWrite", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test5_delete(self):
        """Test deleting a chat"""
        assert TestTeamChats.target_chat is not None
        chat = TestTeamChats.target_chat
        chat.delete_object().execute_query_retry()
