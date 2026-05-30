from tests import test_tenant
from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestTenant(GraphApplicationTestCase):
    @requires_application("Organization.Read.All")
    def test1_find_tenant_information(self):
        """Find tenant information by domain name"""
        result = self.client.tenant_relationships.find_tenant_information_by_domain_name(test_tenant).execute_query()
        self.assertIsNotNone(result.value)
