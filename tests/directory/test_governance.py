from unittest import TestCase

from office365.graph_client import GraphClient

from tests import test_client_id, test_client_secret, test_tenant
from tests.graph_case import GraphSecretTestCase


class TestIdentityGovernance(GraphSecretTestCase):
    def test1_list_app_consent_requests(self):
        result = self.client.identity_governance.app_consent.app_consent_requests.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test2_list_role_assignment_requests(self):
    #    result = (
    #        self.client.role_management.directory.role_assignment_schedule_requests().get().execute_query()
    #    )
    #    self.assertIsNotNone(result.resource_path)
