from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestDeviceManagement(GraphTestCase):

    @requires_delegated_permission(
        "DeviceManagementServiceConfig.Read.All",
        "DeviceManagementServiceConfig.ReadWrite.All",
    )
    def test1_get(self):
        result = self.client.device_management.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test2_get_effective_permissions(self):
    #    result = self.client.device_management.get_effective_permissions().execute_query()
    #    self.assertIsNotNone(result.value)
