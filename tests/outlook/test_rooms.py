from tests.decorators import requires_app_permission
from tests.graph_case import GraphSecretTestCase


class TestRooms(GraphSecretTestCase):
    """Tests for Rooms"""

    @requires_app_permission("Place.Read.All")
    def test1_get_room_lists(self):
        result = self.client.room_lists.get().execute_query()
        self.assertIsNotNone(result.resource_path)
