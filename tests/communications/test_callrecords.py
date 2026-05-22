from tests.decorators import requires_delegated
from tests.graph_case import GraphApplicationTestCase


class TestCallRecord(GraphApplicationTestCase):
    @requires_delegated("CallRecords.Read.All", or_roles=["Global Administrator"])
    def test2_get_direct_routing_calls(self):
        """Gets direct routing call records"""
        result = self.client.communications.call_records.get_direct_routing_calls().execute_query()
        self.assertIsNotNone(result.value)
