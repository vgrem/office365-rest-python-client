from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestMachineLearningHub(SPTestCase):
    """Machine learning hub tests"""

    def test_01_enabled(self):
        """Check if machine learning is enabled"""
        result = self.client.machine_learning.machine_learning_enabled.get().execute_query()
        self.assertIsNotNone(result)

    def test_02_get_default_content_center_site(self):
        """Get the default content center site (placeholder)"""
        # from office365.sharepoint.client_context import ClientContext
        # from tests import test_admin_site_url
        # from tests import test_admin_credentials
        # admin_client = ClientContext(test_admin_site_url).with_credentials(test_admin_credentials)
        # tenant = admin_client.tenant.select(["DefaultContentCenterSite"]).get().execute_query()
        # self.assertIsNotNone(tenant.default_content_center_site)
        pass
