"""Devices — listing, delta, properties, and registered owners.

Tests cover:
  - Listing all devices
  - Getting device delta (changes)
  - Device property assertions (displayName, operatingSystem)
  - Listing registered owners of an existing device

Note: a device object cannot be created through Microsoft Graph by a third-party
app. ``POST /devices`` requires ``alternativeSecurityIds``, and writing that
property is reserved for first-party applications — Graph answers
``Authorization_RequestDenied: Only first-party applications can write
alternative security identifiers on devices`` no matter which licence or
permission the caller holds. Devices exist because they were enrolled, so these
tests read a device the tenant already has.
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.intune.devices.device import Device
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDevices(GraphDelegatedTestCase):
    """Device reads and ownership."""

    device: ClassVar[Optional[Device]] = None

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
        "Device.Read.All",
        "Directory.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_03_device_has_expected_properties(self):
        """A listed device exposes displayName, operatingSystem, and deviceId."""
        device = self._first_device()
        if device is None:
            self.skipTest("The tenant holds no device object")

        self.assertIsNotNone(device.get_property("displayName"))
        self.assertIsNotNone(device.get_property("operatingSystem"))
        self.assertIsNotNone(device.get_property("deviceId"))

    @requires_delegated(
        "Device.Read.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_04_list_registered_owners(self):
        """Listing registered owners of a device returns a valid collection."""
        device = self._first_device()
        if device is None:
            self.skipTest("The tenant holds no device object")

        owners = device.registered_owners.get().execute_query()
        self.assertIsNotNone(owners.resource_path)

    @classmethod
    def _first_device(cls) -> Optional[Device]:
        """The device every read below starts from, listed once."""
        if cls.device is None:
            devices = cls.client.devices.top(1).get().execute_query()
            cls.device = devices[0] if len(devices) else None
        return cls.device
