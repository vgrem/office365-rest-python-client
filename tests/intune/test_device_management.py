from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestDeviceManagement(GraphDelegatedTestCase):
    @requires_delegated_permission_or_role(
        "DeviceManagementServiceConfig.Read.All",
        "DeviceManagementServiceConfig.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test1_get(self):
        """Test retrieving device management settings."""
        result = self.client.device_management.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test2_get_effective_permissions(self):
    #    result = self.client.device_management.get_effective_permissions().execute_query()
    #    self.assertIsNotNone(result.value)
