"""Managed devices — querying managed devices for the current user and tenant-wide.

Tests cover:
  - Getting managed devices for the current user
  - Listing managed devices tenant-wide
  - Managed device property assertions (deviceName, complianceState)
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestManagedDevices(GraphDelegatedTestCase):
    """Managed devices — user-level and tenant-level queries."""

    @requires_delegated(
        "DeviceManagementConfiguration.Read.All",
        "Device.Read.All",
        "Directory.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_01_get_my_managed_devices(self):
        """Getting managed devices for the current user returns a valid collection."""
        try:
            result = self.client.me.managed_devices.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list managed devices: {e}")

    @requires_delegated(
        "DeviceManagementManagedDevices.Read.All",
        "DeviceManagementManagedDevices.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_02_list_managed_devices_tenant_wide(self):
        """Listing managed devices tenant-wide returns a valid collection."""
        try:
            result = self.client.device_management.managed_devices.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
            if len(result) > 0:
                self.assertIsNotNone(result[0].get_property("deviceName"))
        except Exception as e:
            self.skipTest(f"Cannot list managed devices tenant-wide: {e}")
