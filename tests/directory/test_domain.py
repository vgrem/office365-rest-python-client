from office365.directory.domains.domain import Domain

from tests.graph_case import GraphSecretTestCase


class TestDomain(GraphSecretTestCase):
    """Tests for Azure Active Directory (Azure AD) domains"""

    target_domain: Domain = None

    def test1_list_domains(self):
        domains = self.client.domains.top(1).get().execute_query()
        self.assertIsNotNone(domains.resource_path)
        self.assertEqual(len(domains), 1)
        self.__class__.target_domain = domains[0]

    # def test2_verify_domain(self):
    #    domain = self.__class__.target_domain.verify().execute_query()
    #    self.assertIsNotNone(domain.resource_path)
