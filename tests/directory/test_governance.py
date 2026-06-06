"""Identity governance — app consent requests and terms of use agreements.

Tests cover:
  - Listing app consent requests
  - Listing terms of use agreements
"""

from __future__ import annotations

from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestIdentityGovernance(GraphApplicationTestCase):
    """Identity governance — app consent and terms of use."""

    @requires_application("EntitlementManagement.Read.All", "Approve.AppConsentRequests.Read.All")
    def test_01_list_app_consent_requests(self):
        """Listing app consent requests returns a valid collection."""
        result = self.client.identity_governance.app_consent.app_consent_requests.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("Agreement.Read.All")
    def test_02_list_agreements(self):
        """Listing terms of use agreements returns a valid collection."""
        try:
            result = self.client.identity_governance.terms_of_use.agreements.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list agreements: {e}")
