from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestIntuneReports(GraphTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestIntuneReports, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated_permission("DeviceManagementConfiguration.Read.All")
    def test1_device_configuration_user_activity(self):
        result = (
            self.client.reports.device_configuration_user_activity().execute_query()
        )
        self.assertIsNotNone(result.value)
