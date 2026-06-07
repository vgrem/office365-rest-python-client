"""Tests for SharePoint workflow services including manager retrieval."""

from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestWorkflows(SPTestCase):
    """Test SharePoint workflow features."""

    def test_01_get_manager(self):
        """Get the workflow services manager."""
        manager = self.client.workflow_services_manager.get().execute_query()
        self.assertIsNotNone(manager.resource_path)

    # def test2_enumerate_definitions(self):
    #    manager = self.client.workflow_deployment_service.enumerate_definitions().execute_query()
    #    self.assertIsNotNone(manager.resource_path)
