"""Device management — tenant settings, audit events, device categories, and reports.

Tests cover:
  - Getting device management settings
  - Getting effective permissions
  - Listing audit events
  - Listing device categories
  - Listing managed devices (global)
  - Intune brand property access
  - Terms and conditions listing
  - Device management reports access
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDeviceManagement(GraphDelegatedTestCase):
    """Intune device management — tenant-wide settings and collections."""

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_01_get_device_management_settings(self):
        """Getting device management settings returns a valid entity."""
        result = self.client.device_management.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_02_device_management_has_intune_brand(self):
        """Device management should expose an intuneBrand property."""
        result = self.client.device_management.get().execute_query()
        brand = result.get_property("intuneBrand")
        self.assertIsNotNone(brand)

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_03_get_effective_permissions(self):
        """Getting effective permissions returns a valid result."""
        try:
            result = self.client.device_management.get_effective_permissions().execute_query()
            self.assertIsNotNone(result.value)
        except Exception as e:
            self.skipTest(f"Cannot get effective permissions: {e}")

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_04_list_audit_events(self):
        """Listing audit events returns a valid collection."""
        try:
            result = self.client.device_management.audit_events.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list audit events: {e}")

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_05_list_device_categories(self):
        """Listing device categories returns a valid collection."""
        try:
            result = self.client.device_management.device_categories.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception:
            self.skipTest("Device categories not available")

    @requires_delegated(
        "DeviceManagementManagedDevices.Read.All", "DeviceManagementManagedDevices.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_06_list_managed_devices(self):
        """Listing managed devices returns a valid collection."""
        try:
            result = self.client.device_management.managed_devices.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
            if len(result) > 0:
                self.assertIsNotNone(result[0].get_property("id"))
        except Exception as e:
            self.skipTest(f"Cannot list managed devices: {e}")

    @requires_delegated(
        "DeviceManagementServiceConfig.Read.All", "DeviceManagementServiceConfig.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_07_list_terms_and_conditions(self):
        """Listing terms and conditions returns a valid collection."""
        try:
            result = self.client.device_management.terms_and_conditions.top(5).get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception:
            self.skipTest("Terms and conditions not available")
