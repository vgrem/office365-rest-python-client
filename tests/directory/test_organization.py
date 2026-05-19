from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphApplicationTestCase


class TestOrganization(GraphApplicationTestCase):
    @requires_delegated_permission_or_role("Organization.Read.All", roles=["Global Administrator"])
    def test1_list(self):
        """List organization"""
        org = self.client.organization.get().execute_query()
        self.assertIsNotNone(org.resource_path)

    @requires_delegated_permission_or_role("Organization.Read.All", roles=["Global Administrator"])
    def test2_list_contacts(self):
        """List organization contacts"""
        result = self.client.contacts.get().top(10).execute_query()
        self.assertIsNotNone(result.resource_path)
