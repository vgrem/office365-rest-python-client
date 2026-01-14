from unittest import TestCase

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant
from tests.decorators import requires_app_permission


class TestAudit(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    @requires_app_permission("AuditLog.Read.All")
    def test1_list_signins(self):
        col = self.client.audit_logs.signins.top(10).get().execute_query()
        self.assertIsNotNone(col.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test2_list_directory_audits(self):
        col = self.client.audit_logs.directory_audits.top(10).get().execute_query()
        self.assertIsNotNone(col.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test3_list_provisioning(self):
        col = self.client.audit_logs.provisioning.top(10).get().execute_query()
        self.assertIsNotNone(col.resource_path)
