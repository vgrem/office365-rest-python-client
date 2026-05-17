from tests import test_tenant
from tests.graph_case import GraphSecretTestCase


class TestTenant(GraphSecretTestCase):
    def test1_find_tenant_information(self):
        result = self.client.tenant_relationships.find_tenant_information_by_domain_name(test_tenant).execute_query()
        self.assertIsNotNone(result.value)
