from unittest import TestCase

from office365.graph_client import GraphClient

from tests import test_client_id, test_client_secret, test_tenant
from tests.decorators import requires_app_permission
from tests.graph_case import GraphSecretTestCase


class TestAudit(GraphSecretTestCase):
    @requires_app_permission("AuditLog.Read.All")
    def test1_list_signins(self):
        result = self.client.audit_logs.signins.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test2_list_directory_audits(self):
        result = self.client.audit_logs.directory_audits.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test3_list_provisioning(self):
        result = self.client.audit_logs.provisioning.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)
