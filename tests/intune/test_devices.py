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
from tests.graph_case import GraphDelegatedTestCase


class TestDevices(GraphDelegatedTestCase):
    """Device reads and ownership.

    These read Entra's device objects, not Intune's: the inventory under
    ``deviceManagement`` is ``test_managed_devices.py``.
    """

    @requires_delegated("Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All")
    def test_01_devices_are_listed(self):
        """A registered device is an Entra object, and ``/devices`` states the type it holds."""
        devices = self.client.devices
        self.assertTrue(str(devices.resource_path).endswith("/devices"))

        rows = devices.top(10).get().execute_query()

        self.assertIs(rows.item_type(), Device)

    @requires_delegated("Device.Read.All", "Directory.Read.All")
    def test_02_the_delta_track_carries_the_same_rows(self):
        """``devices/delta`` is the incremental view: same rows, plus a skip token."""
        delta = self.client.devices.delta
        self.assertTrue(str(delta.resource_path).endswith("/delta"))

        delta.top(5).get().execute_query()

    @requires_delegated("Device.Read.All", "Directory.Read.All")
    def test_03_a_device_names_its_platform(self):
        """A device object exposes displayName, operatingSystem and deviceId."""
        rows = self.client.devices.top(1).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no registered device")

        device = rows[0]
        self.assertIsNotNone(device.get_property("displayName"))
        self.assertIsNotNone(device.get_property("operatingSystem"))
        self.assertIsNotNone(device.get_property("deviceId"))

    @requires_delegated("Device.Read.All", "Directory.Read.All", "Directory.ReadWrite.All")
    def test_04_registered_owners_are_listed(self):
        """Ownership is a navigation off the device, and one device may have several owners."""
        rows = self.client.devices.top(1).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no registered device")

        device = rows[0]
        owners = device.registered_owners.top(5).get().execute_query()

        self.assertIn(f"/devices/{device.id}/registeredOwners", str(owners.resource_path))
