from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestIdentityGovernance(GraphApplicationTestCase):
    @requires_application("EntitlementManagement.Read.All", "Approve.AppConsentRequests.Read.All")
    def test1_list_app_consent_requests(self):
        """List app consent requests"""
        result = self.client.identity_governance.app_consent.app_consent_requests.get().execute_query()
        self.assertIsNotNone(result.resource_path)
