from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestReports(GraphTestCase):

    @requires_delegated_permission("Reports.Read.All")
    def test1_get_office365_activations_user_counts(self):
        result = self.client.reports.get_office365_activations_user_counts().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("AuditLog.Read.All")
    def test2_list_user_registration_details(self):
        result = self.client.reports.authentication_methods.user_registration_details.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("AuditLog.Read.All")
    def test3_list_users_registered_by_method(self):
        result = self.client.reports.authentication_methods.users_registered_by_method().execute_query()
        self.assertIsNotNone(result.value)
