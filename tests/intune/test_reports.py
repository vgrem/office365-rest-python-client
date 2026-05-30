from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestIntuneReports(GraphDelegatedTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", bypass_roles=["Global Administrator"])
    def test1_device_configuration_user_activity(self):
        """Test retrieving device configuration user activity report."""
        result = self.client.reports.device_configuration_user_activity().execute_query()
        self.assertIsNotNone(result.value)
