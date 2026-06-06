"""Audit log queries — sign-ins, directory audits, and provisioning logs.

Tests cover:
  - Listing sign-in logs
  - Listing directory audit logs
  - Listing provisioning logs
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestAudit(GraphApplicationTestCase):
    """Audit log queries — sign-ins, directory audits, and provisioning."""

    @requires_application("AuditLog.Read.All")
    def test_01_list_signins(self):
        """Listing top 10 sign-in logs returns a valid collection."""
        result = self.client.audit_logs.signins.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("AuditLog.Read.All", "Directory.Read.All")
    def test_02_list_directory_audits(self):
        """Listing top 10 directory audit logs returns a valid collection."""
        result = self.client.audit_logs.directory_audits.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("AuditLog.Read.All", "Directory.Read.All")
    def test_03_list_provisioning(self):
        """Listing top 10 provisioning logs returns a valid collection."""
        result = self.client.audit_logs.provisioning.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)
