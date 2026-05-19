from typing import Optional

from office365.communications.presences.presence import Presence
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPresence(GraphDelegatedTestCase):
    target_presence: Optional[Presence] = None

    @requires_delegated("Presence.ReadWrite", or_roles=["Global Administrator"])
    def test1_get_my_presence(self):
        """Gets the current user's presence"""
        result = self.client.me.presence.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Presence.ReadWrite", or_roles=["Global Administrator"])
    def test2_set_my_preferred_presence(self):
        """Sets the current user's preferred presence"""
        result = self.client.me.presence.set_user_preferred_presence().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Presence.ReadWrite", or_roles=["Global Administrator"])
    def test3_get_presences_by_user_id(self):
        """Gets presences by user IDs"""
        me = self.client.me.get().execute_query()
        assert me.id is not None, "User ID must not be None"
        result = self.client.communications.get_presences_by_user_id([me.id]).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Presence.ReadWrite", or_roles=["Global Administrator"])
    def test4_set_status_message(self):
        """Sets the current user's status message"""
        result = self.client.me.presence.set_status_message("Hey I'm currently in a meeting").execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Presence.ReadWrite", or_roles=["Global Administrator"])
    def test5_clear_my_presence(self):
        """Clears the current user's preferred presence"""
        result = self.client.me.presence
        result.clear_user_preferred_presence().execute_query()
        self.assertIsNotNone(result.resource_path)
