from typing import Optional

from office365.directory.domains.domain import Domain

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestDomain(GraphApplicationTestCase):
    """Tests for Azure Active Directory (Azure AD) domains"""

    target_domain: Optional[Domain] = None

    @requires_application("Domain.Read.All")
    def test1_list_domains(self):
        """List domains"""
        domains = self.client.domains.top(1).get().execute_query()
        self.assertIsNotNone(domains.resource_path)
        self.assertEqual(len(domains), 1)
        TestDomain.target_domain = domains[0]
