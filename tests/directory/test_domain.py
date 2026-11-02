"""Domains — listing and property access.

Tests cover:
  - Listing domains (top 1)
  - Accessing domain properties (id, supported services)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.domains.domain import Domain

from tests import test_tenant
from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestDomain(GraphApplicationTestCase):
    """Azure AD domain listing and property access."""

    target_domain: ClassVar[Optional[Domain]] = None

    @requires_application("Domain.Read.All")
    def test_01_list_domains(self):
        """The tenant's own domain is in the list, and a domain can be picked for later tests.

        ``$top`` was asked for once and the service answered with two entries, so the
        count is not the fact worth pinning; the tenant domain being present is.
        """
        domains = self.client.domains.get().execute_query()
        self.assertGreater(len(domains), 0)
        self.assertIn(test_tenant, [d.id for d in domains])
        default = [d for d in domains if d.get_property("isDefault")]
        TestDomain.target_domain = default[0] if default else domains[0]

    @requires_application("Domain.Read.All")
    def test_02_domain_has_properties(self):
        """A domain entry exposes id and supportedServices."""
        domain = TestDomain.target_domain
        if not domain:
            self.skipTest("No domain retrieved from list")
        self.assertIsNotNone(domain.id)
        self.assertIsNotNone(domain.supported_services)
