"""Tests for SharePoint feature operations (site and web feature listing)."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.features.feature import Feature

from tests.sharepoint.sharepoint_case import SPTestCase


class TestFeature(SPTestCase):
    """Tests for SharePoint feature enumeration and retrieval."""

    result_feature: ClassVar[Optional[Feature]] = None

    def test_01_list_site_features(self):
        """List all features enabled on the site."""
        result = self.client.site.features.get().execute_query()
        self.assertGreater(len(result), 0)
        TestFeature.result_feature = result[0]

    def test_02_get_site_feature(self):
        """Get a specific site feature by its ID."""
        target = TestFeature.result_feature
        if not target:
            self.skipTest("No resource from previous test")
        result = target.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_03_list_web_features(self):
        """List all features enabled on the root web."""
        result = self.client.site.root_web.features.get().execute_query()
        self.assertGreater(len(result), 0)
