"""Domains — listing and property access.

Tests cover:
  - Listing domains (top 1)
  - Accessing domain properties (id, supported services)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.domains.domain import Domain

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestDomain(GraphApplicationTestCase):
    """Azure AD domain listing and property access."""

    target_domain: ClassVar[Optional[Domain]] = None

    @requires_application("Domain.Read.All")
    def test_01_list_domains(self):
        """Listing top 1 domain returns a valid collection."""
        domains = self.client.domains.top(1).get().execute_query()
        self.assertIsNotNone(domains.resource_path)
        self.assertEqual(len(domains), 1)
        TestDomain.target_domain = domains[0]

    @requires_application("Domain.Read.All")
    def test_02_domain_has_properties(self):
        """A domain entry exposes id and supportedServices."""
        domain = TestDomain.target_domain
        if not domain:
            self.skipTest("No domain retrieved from list")
        self.assertIsNotNone(domain.id)
        self.assertIsNotNone(domain.supported_services)
