"""Tests for SharePoint alerts (web alerts and user alerts)."""

from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestAlert(SPTestCase):
    """Tests for SharePoint alert operations."""

    def test_01_get_web_alerts(self):
        """Get alerts for the current web."""
        alerts = self.client.web.alerts.get().execute_query()
        self.assertIsNotNone(alerts.resource_path)

    def test_02_get_user_alerts(self):
        """Get alerts for the current user."""
        alerts = self.client.web.current_user.alerts.get().execute_query()
        self.assertIsNotNone(alerts.resource_path)
