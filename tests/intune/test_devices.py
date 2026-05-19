from __future__ import annotations

from typing import Optional

from office365.intune.devices.device import Device
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDevices(GraphDelegatedTestCase):
    device: Optional[Device] = None

    @requires_delegated(
        "Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test3_list_devices(self):
        """Test listing all devices."""
        result = self.client.devices.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "DeviceManagementConfiguration.Read.All",
        "Device.Read.All",
        "Directory.Read.All",
        or_roles=["Global Administrator"],
    )
    def test4_get_delta(self):
        """Test getting device delta."""
        result = self.client.devices.delta.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Directory.AccessAsUser.All", or_roles=["Global Administrator"])
    def test5_create_device(self):
        """Test creating a new device."""
        result = self.client.devices.add("Test device", "linux", "1").execute_query()
        self.assertIsNotNone(result.resource_path)
        TestDevices.device = result

    @requires_delegated("Directory.AccessAsUser.All", or_roles=["Global Administrator"])
    def test6_add_registered_owner(self):
        """Test adding a registered owner to a device."""
        assert TestDevices.device is not None
        result = TestDevices.device.registered_owners.add(self.client.me).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Device.Read.AllDirectory.Read.All", "Directory.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test7_list_registered_owners(self):
        """Test listing registered owners of a device."""
        assert TestDevices.device is not None
        result = TestDevices.device.registered_owners.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Directory.AccessAsUser.All", or_roles=["Global Administrator"])
    def test8_delete_device(self):
        """Test deleting a device."""
        assert TestDevices.device is not None
        TestDevices.device.delete_object().execute_query()
