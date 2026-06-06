from __future__ import annotations

from office365.sharepoint.multigeo.api_versions import MultiGeoApiVersions

from tests.sharepoint.sharepoint_case import SPTestCase


class TestMultiGeo(SPTestCase):
    """Multi-geo tests"""

    def test_01_get_api_versions(self):
        """Get multi-geo API versions"""
        result = MultiGeoApiVersions(self.client).get().execute_query()
        self.assertTrue(result.resource_path)
