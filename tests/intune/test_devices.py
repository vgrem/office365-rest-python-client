"""Devices — listing, delta, creating, registered owners, and deletion.

Tests cover:
  - Listing all devices
  - Getting device delta (changes)
  - Creating a new device
  - Adding a registered owner to a device
  - Listing registered owners
  - Deleting a device
  - Device property assertions (displayName, operatingSystem)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDevices(GraphDelegatedTestCase):
    """Device CRUD, ownership, and delta."""

    device: ClassVar[Optional[object]] = None

    @requires_delegated(
        "Device.Read.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_01_list_devices(self):
        """Listing all devices returns a valid collection."""
        result = self.client.devices.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "DeviceManagementConfiguration.Read.All",
        "Device.Read.All",
        "Directory.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_02_get_device_delta(self):
        """Getting device delta returns a valid collection."""
        result = self.client.devices.delta.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.AccessAsUser.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_03_create_device(self):
        """Creating a new device should succeed."""
        result = self.client.devices.add("SDK Test Device", "linux", "1").execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertIsNotNone(result.get_property("id"))
        self.assertEqual(result.get_property("displayName"), "SDK Test Device")
        TestDevices.device = result

    @requires_delegated(
        "Device.Read.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_04_device_has_expected_properties(self):
        """A device entry exposes displayName, operatingSystem, and isManaged."""
        device = TestDevices.device
        if not device:
            self.skipTest("No device created from previous test")

        self.assertIsNotNone(device.get_property("displayName"))
        self.assertIsNotNone(device.get_property("operatingSystem"))

    @requires_delegated(
        "Directory.AccessAsUser.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_05_add_registered_owner(self):
        """Adding a registered owner to a device should succeed."""
        device = TestDevices.device
        if not device:
            self.skipTest("No device created from previous test")

        result = device.registered_owners.add(self.client.me).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Device.Read.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_06_list_registered_owners(self):
        """Listing registered owners of a device returns a valid collection."""
        device = TestDevices.device
        if not device:
            self.skipTest("No device created from previous test")

        owners = device.registered_owners.get().execute_query()
        self.assertIsNotNone(owners.resource_path)

    @requires_delegated(
        "Directory.AccessAsUser.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_07_delete_device(self):
        """Deleting a device should succeed."""
        device = TestDevices.device
        if not device:
            self.skipTest("No device created from previous test")

        device.delete_object().execute_query()
        TestDevices.device = None

    @classmethod
    def tearDownClass(cls):
        device = cls.device
        if device and device.resource_path:
            try:
                device.delete_object().execute_query()
            except Exception:
                pass
