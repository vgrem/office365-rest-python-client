from office365.intune.devices.device import Device
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestDevices(GraphTestCase):
    device = None  # type: Device

    @requires_delegated_permission(
        "Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All"
    )
    def test3_list_devices(self):
        result = self.client.devices.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    #@requires_delegated_permission("Device.Read.All")
    def test4_get_delta(self):
        result = self.client.devices.delta.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Directory.AccessAsUser.All")
    def test5_create_device(self):
        result = self.client.devices.add("Test device", "linux", "1").execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.device = result

    @requires_delegated_permission("Directory.AccessAsUser.All")
    def test6_add_registered_owner(self):
        result = self.__class__.device.registered_owners.add(
            self.client.me
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission(
        "Device.Read.All" "Directory.Read.All", "Directory.ReadWrite.All"
    )
    def test7_list_registered_owners(self):
        result = self.__class__.device.registered_owners.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Directory.AccessAsUser.All")
    def test8_delete_device(self):
        self.__class__.device.delete_object().execute_query()
