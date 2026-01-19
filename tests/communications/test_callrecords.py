from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant
from tests.graph_case import GraphSecretTestCase


class TestCallRecord(GraphSecretTestCase):
    @classmethod
    def tearDownClass(cls):
        pass

    # def test1_create_peer_to_peer_call(self):
    #    result = self.client.communications.calls.create("https://bot.mediadev8.com/callback").execute_query()
    #    self.assertIsNotNone(result.resource_path)

    def test2_get_direct_routing_calls(self):
        result = self.client.communications.call_records.get_direct_routing_calls().execute_query()
        self.assertIsNotNone(result.value)
