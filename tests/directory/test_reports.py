"""Directory reports — Office 365 activations, authentication method registration details.

Tests cover:
  - Getting Office 365 activations user counts
  - Listing user registration details
  - Listing users registered by authentication method
  - Getting users registered by feature
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestReports(GraphDelegatedTestCase):
    """Directory reports — activation counts and authentication method registration."""

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Reports Reader", "Global Reader", "Global Administrator"],
    )
    def test_01_get_office365_activations_user_counts(self):
        """Getting Office 365 activations user counts returns a value."""
        result = self.client.reports.get_office365_activations_user_counts().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "AuditLog.Read.All",
        bypass_roles=["Security Administrator", "Security Reader", "Global Reader", "Global Administrator"],
    )
    def test_02_list_user_registration_details(self):
        """Listing user registration details returns a valid collection."""
        result = self.client.reports.authentication_methods.user_registration_details.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "AuditLog.Read.All",
        bypass_roles=["Security Administrator", "Security Reader", "Global Reader", "Global Administrator"],
    )
    def test_03_list_users_registered_by_method(self):
        """Listing users registered by authentication method returns a value."""
        result = self.client.reports.authentication_methods.users_registered_by_method().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "AuditLog.Read.All",
        bypass_roles=["Security Administrator", "Security Reader", "Global Reader", "Global Administrator"],
    )
    def test_04_users_registered_by_feature(self):
        """Getting users registered by feature returns a value."""
        result = self.client.reports.authentication_methods.users_registered_by_feature().execute_query()
        self.assertIsNotNone(result.value)
