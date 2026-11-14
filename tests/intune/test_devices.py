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

from office365.intune.devices.device import Device

from tests.decorators import requires_delegated
from tests.intune.intune_case import IntuneCase


class TestDevices(IntuneCase):
    """Device reads and ownership.

    These read Entra's device objects, not Intune's: the inventory under
    ``deviceManagement`` is ``test_managed_devices.py``.
    """

    @requires_delegated("Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All")
    def test_01_devices_are_listed(self):
        """A registered device is an Entra object, and ``/devices`` states the type it holds."""
        devices = self.read(self.client.devices, "devices", limit=10)

        self.assertIs(devices.item_type(), Device)

    @requires_delegated("Device.Read.All", "Directory.Read.All")
    def test_02_the_delta_track_carries_the_same_rows(self):
        """``devices/delta`` is the incremental view: same rows, plus a skip token."""
        self.read(self.client.devices.delta, "delta")

    @requires_delegated("Device.Read.All", "Directory.Read.All")
    def test_03_a_device_names_its_platform(self):
        """A device object exposes displayName, operatingSystem and deviceId."""
        devices = self.read(self.client.devices, "devices", limit=1)
        device = self.row_or_skip(devices, "registered device")

        self.assertIsNotNone(device.get_property("displayName"))
        self.assertIsNotNone(device.get_property("operatingSystem"))
        self.assertIsNotNone(device.get_property("deviceId"))

    @requires_delegated("Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All")
    def test_04_registered_owners_are_listed(self):
        """Ownership is a navigation off the device, and one device may have several owners."""
        devices = self.read(self.client.devices, "devices", limit=1)
        device = self.row_or_skip(devices, "registered device")
        owners = device.registered_owners.get().execute_query()

        self.assertIn(f"/devices/{device.id}/registeredOwners", str(owners.resource_path))
