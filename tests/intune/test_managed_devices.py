from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestManagedDevices(GraphDelegatedTestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class."""

    # def test1_create(self):
    #    result = self.client.device_management.managed_devices.add().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role(
        "DeviceManagementConfiguration.Read.All", "Device.Read.All", "Directory.Read.All", roles=["Global Administrator"]
    )
    def test2_get_my(self):
        """Test retrieving managed devices for the current user."""
        result = self.client.me.managed_devices.get().execute_query()
        self.assertIsNotNone(result.resource_path)
