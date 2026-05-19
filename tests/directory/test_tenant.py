from tests import test_tenant
from tests.decorators import requires_delegated
from tests.graph_case import GraphApplicationTestCase


class TestTenant(GraphApplicationTestCase):
    @requires_delegated("Organization.Read.All", or_roles=["Global Administrator"])
    def test1_find_tenant_information(self):
        """Find tenant information by domain name"""
        result = self.client.tenant_relationships.find_tenant_information_by_domain_name(test_tenant).execute_query()
        self.assertIsNotNone(result.value)
