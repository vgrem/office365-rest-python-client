from tests.decorators import requires_app_permission
from tests.graph_case import GraphApplicationTestCase


class TestAudit(GraphApplicationTestCase):
    @requires_app_permission("AuditLog.Read.All")
    def test1_list_signins(self):
        """List sign-in logs"""
        result = self.client.audit_logs.signins.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test2_list_directory_audits(self):
        """List directory audit logs"""
        result = self.client.audit_logs.directory_audits.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_app_permission("AuditLog.Read.All", "Directory.Read.All")
    def test3_list_provisioning(self):
        """List provisioning logs"""
        result = self.client.audit_logs.provisioning.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)
