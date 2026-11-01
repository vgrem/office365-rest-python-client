"""Tenant information — finding tenant information by domain name.

Tests cover:
  - Finding tenant information by domain name
"""

from __future__ import annotations

from office365.directory.tenantinformation.relationship import TenantRelationship

from tests import test_tenant
from tests.decorators import requires_call
from tests.graph_case import GraphApplicationTestCase


class TestTenant(GraphApplicationTestCase):
    """Tenant information lookup by domain name."""

    @requires_call(
        TenantRelationship.find_tenant_information_by_domain_name,
        flow="application",
    )
    def test_01_find_tenant_information(self):
        """Finding tenant information by domain name returns a value."""
        result = self.client.tenant_relationships.find_tenant_information_by_domain_name(test_tenant).execute_query()
        self.assertIsNotNone(result.value)
