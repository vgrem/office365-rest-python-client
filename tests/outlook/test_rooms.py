from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestRooms(GraphApplicationTestCase):
    """Tests for Rooms"""

    @requires_application("Place.Read.All")
    def test1_get_room_lists(self):
        result = self.client.room_lists.get().execute_query()
        self.assertIsNotNone(result.resource_path)
