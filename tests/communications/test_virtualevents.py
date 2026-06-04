from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestVirtualEvents(GraphDelegatedTestCase):
    @requires_delegated("VirtualEvent.Read", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test1_list_webinars(self):
        """Lists virtual event webinars"""
        webinars = self.client.solutions.virtual_events.webinars.top(10).get().execute_query()
        self.assertIsNotNone(webinars)

    @requires_delegated("VirtualEvent.Read", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test2_list_townhalls(self):
        """Lists virtual event town halls"""
        townhalls = self.client.solutions.virtual_events.townhalls.top(10).get().execute_query()
        self.assertIsNotNone(townhalls)
