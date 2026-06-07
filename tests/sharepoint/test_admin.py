"""Tests for SharePoint admin operations (tenant-level administration)."""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant

from tests import (
    test_admin_site_url,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestAdmin(SPTestCase):
    """Tests for SharePoint tenant admin operations."""

    @classmethod
    def setUpClass(cls):
        cls.client = ClientContext(test_admin_site_url).with_username_and_password(
            test_tenant,
            test_client_id,
            test_username,
            test_password,
        )
        cls.tenant = Tenant(cls.client)

    def test_01_get_analytics_usage(self):
        """Get analytics usage service for the tenant."""
        from office365.sharepoint.administration.analytics.usage_service import (
            SPAnalyticsUsageService,
        )

        analytics = SPAnalyticsUsageService(self.client).get().execute_query()
        self.assertIsNotNone(analytics.resource_path)

    # def test2_render_policy_report(self):
    #    result = self.tenant.render_policy_report().execute_query()
    #    self.assertIsNotNone(result.value)

    # def test3_render_recent_admin_actions(self):
    #    result = self.tenant.render_recent_admin_actions().execute_query()
    #    self.assertIsNotNone(result.value)

    def test_02_set_file_version_policy(self):
        """Set file version policy on the tenant."""
        result = self.tenant.set_file_version_policy(True, 100, 10).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_03_get_file_version_policy(self):
        """Get file version policy from the tenant."""
        result = self.tenant.get_file_version_policy().execute_query()
        self.assertIsNotNone(result.value)

    def test_04_clear_file_version_policy(self):
        """Clear file version policy on the tenant."""
        result = self.tenant.clear_file_version_policy().execute_query()
        self.assertIsNotNone(result.resource_path)

    # requires SharePoint Advanced Management license
    # def test7_get_ransomware_activities(self):
    #    result = self.tenant.get_ransomware_activities().execute_query()
    #    self.assertIsNotNone(result.value)

    def test_05_get_root_site_url(self):
        """Get root site URL from the tenant."""
        result = self.tenant.get_root_site_url().execute_query()
        self.assertIsNotNone(result.value)

    # def test9_get_app_service_principal(self):
    #    result = self.tenant.app_service_principal.get().execute_query()
    #    self.assertIsNotNone(result.resource_path)
