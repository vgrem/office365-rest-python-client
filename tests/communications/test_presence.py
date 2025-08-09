from office365.communications.presences.presence import Presence
from tests.graph_case import GraphTestCase


class TestPresence(GraphTestCase):
    target_presence: Presence = None

    def test1_get_my_presence(self):
        result = self.client.me.presence.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test2_set_my_preferred_presence(self):
        result = self.client.me.presence.set_user_preferred_presence().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_get_presences_by_user_id(self):
        me = self.client.me.get().execute_query()
        result = self.client.communications.get_presences_by_user_id(
            [me.id]
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test4_set_status_message(self):
        result = self.client.me.presence.set_status_message(
            "Hey I'm currently in a meeting"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test5_clear_my_presence(self):
        result = self.client.me.presence
        result.clear_user_preferred_presence().execute_query()
        self.assertIsNotNone(result.resource_path)
