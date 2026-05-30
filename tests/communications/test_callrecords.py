from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestCallRecord(GraphApplicationTestCase):
    @requires_application("CallRecords.Read.All")
    def test2_get_direct_routing_calls(self):
        """Gets direct routing call records"""
        result = self.client.communications.call_records.get_direct_routing_calls().execute_query()
        self.assertIsNotNone(result.value)
