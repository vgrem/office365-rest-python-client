from office365.teams.chats.chat import Chat
from tests.graph_case import GraphTestCase


class TestTeamChats(GraphTestCase):
    """Tests for team Chats"""

    target_chat: Chat = None

    # def test1_create(self):
    #    new_chat = self.client.chats.add("oneOnOne").execute_query()
    #    self.assertIsNotNone(new_chat.resource_path)
    #    self.__class__.target_chat = new_chat

    def test2_list_user_chats(self):
        result = self.client.me.chats.get().top(1).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 0)

    # def test3_delete(self):
    #    chat = self.__class__.target_chat
    #    chat.delete_object().execute_query()
