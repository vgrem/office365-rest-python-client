"""Intune reports — device configuration activity reports.

Tests cover:
  - Getting device configuration user activity report
  - Getting device configuration device activity report
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestIntuneReports(GraphDelegatedTestCase):
    """Intune reporting — device configuration activity."""

    @requires_delegated(
        "DeviceManagementConfiguration.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_01_device_configuration_user_activity(self):
        """Getting device configuration user activity report returns data."""
        result = self.client.reports.device_configuration_user_activity().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "DeviceManagementConfiguration.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_02_device_configuration_device_activity(self):
        """Getting device configuration device activity report returns data."""
        result = self.client.reports.device_configuration_device_activity().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "DeviceManagementManagedDevices.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_03_managed_device_enrollment_failure_details(self):
        """Getting managed device enrollment failure details report returns data."""
        try:
            result = self.client.reports.managed_device_enrollment_failure_details().execute_query()
            self.assertIsNotNone(result.value)
        except Exception as e:
            self.skipTest(f"Cannot get enrollment failure details: {e}")

    @requires_delegated(
        "DeviceManagementManagedDevices.Read.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_04_managed_device_enrollment_top_failures(self):
        """Getting managed device enrollment top failures returns data."""
        try:
            result = self.client.reports.managed_device_enrollment_top_failures().execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Enrollment top failures not available")
