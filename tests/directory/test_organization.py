"""Organization — listing and contacts.

Tests cover:
  - Listing organization details
  - Listing organization contacts
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestOrganization(GraphApplicationTestCase):
    """Organization listing and contacts."""

    @requires_application("Organization.Read.All")
    def test_01_list(self):
        """Listing organization returns a valid entity."""
        org = self.client.organization.get().execute_query()
        self.assertIsNotNone(org.resource_path)

    @requires_application("Organization.Read.All")
    def test_02_list_contacts(self):
        """Listing organization contacts returns a valid collection."""
        result = self.client.contacts.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)
