"""Intune reports: the ones served by Graph's own report root.

``deviceManagement/reports`` exists as a model and answers ``UnknownError`` on this tenant, and
``reports.managedDeviceEnrollmentFailureDetails`` answers ``500`` - both measured, neither a
statement about the model. What does work is Graph's shared report root, where the Intune
activity reports are exported as a ``ReportResult`` that is fetched as bytes.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, IntuneCase


class TestDeviceActivityReports(IntuneCase):
    """The two per-PC activity exports."""

    @requires_delegated(*CONFIGURATION)
    def test_01_device_configuration_user_activity(self):
        """A user-activity export answers with a report result, not rows."""
        report = self.client.reports.device_configuration_user_activity().execute_query()

        self.assertIsNotNone(report.value)

    @requires_delegated(*CONFIGURATION)
    def test_02_device_configuration_device_activity(self):
        """The device-activity export reads the same shape for the other dimension."""
        report = self.client.reports.device_configuration_device_activity().execute_query()

        self.assertIsNotNone(report.value)
