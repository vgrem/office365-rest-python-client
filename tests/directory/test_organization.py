from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestOrganization(GraphApplicationTestCase):
    @requires_application("Organization.Read.All")
    def test1_list(self):
        """List organization"""
        org = self.client.organization.get().execute_query()
        self.assertIsNotNone(org.resource_path)

    @requires_application("Organization.Read.All")
    def test2_list_contacts(self):
        """List organization contacts"""
        result = self.client.contacts.get().top(10).execute_query()
        self.assertIsNotNone(result.resource_path)
