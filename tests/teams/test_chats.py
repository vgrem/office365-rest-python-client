from office365.teams.chats.chat import Chat
from office365.teams.chats.type import ChatType

from tests import test_user_principal_name
from tests.graph_case import GraphTestCase


class TestTeamChats(GraphTestCase):
    """Tests for team Chats"""

    target_chat: Chat = None

    def test1_create(self):
        owner = self.client.me.get().execute_query()
        another_owner = self.client.users[test_user_principal_name].get().execute_query()

        new_chat = self.client.chats.add(ChatType.oneOnOne, owner_ids=[owner.id, another_owner.id]).execute_query()
        self.assertIsNotNone(new_chat.resource_path)
        self.__class__.target_chat = new_chat

    def test2_list_user_chats(self):
        result = self.client.me.chats.get().top(10).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 0)

    def test3_delete(self):
        chat = self.__class__.target_chat
        chat.delete_object().execute_query()
