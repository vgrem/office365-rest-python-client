from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestReports(GraphDelegatedTestCase):
    @requires_delegated_permission_or_role("Reports.Read.All", roles=["Global Administrator"])
    def test1_get_office365_activations_user_counts(self):
        """Get Office 365 activations user counts"""
        result = self.client.reports.get_office365_activations_user_counts().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role("AuditLog.Read.All", roles=["Global Administrator"])
    def test2_list_user_registration_details(self):
        """List user registration details"""
        result = self.client.reports.authentication_methods.user_registration_details.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role("AuditLog.Read.All", roles=["Global Administrator"])
    def test3_list_users_registered_by_method(self):
        """List users registered by authentication method"""
        result = self.client.reports.authentication_methods.users_registered_by_method().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role("AuditLog.Read.All", roles=["Global Administrator"])
    def test4_users_registered_by_feature(self):
        """Get users registered by feature"""
        result = self.client.reports.authentication_methods.users_registered_by_feature().execute_query()
        self.assertIsNotNone(result.value)
