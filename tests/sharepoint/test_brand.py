"""Tests for SharePoint brand center operations (themes and configuration)."""

from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestBrand(SPTestCase):
    """Tests for SharePoint brand center operations."""

    def test_01_get_site_themes(self):
        """Get site themes from the brand center."""
        result = self.client.brand_center.get_site_themes().execute_query()
        self.assertIsNotNone(result.value)

    def test_02_get_configuration(self):
        """Get brand center configuration."""
        result = self.client.brand_center.configuration().execute_query()
        self.assertIsNotNone(result.value)
