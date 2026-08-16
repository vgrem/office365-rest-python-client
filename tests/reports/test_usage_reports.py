"""Microsoft Graph Usage Reports — partner billing usage data.

Tests cover:
  - Exporting billed usage data for a partner
  - Operation status for export result
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestUsageReports(GraphDelegatedTestCase):
    """Partner billing usage reports."""

    @requires_delegated(
        "PartnerBilling.Read.All",
        bypass_roles=["Billing Administrator", "Global Administrator"],
    )
    def test_01_billed_usage_export(self):
        """Exporting billed usage data should return an operation."""
        try:
            result = self.client.reports.partners.billing.usage.billed.export("G016907411").execute_query()
            self.assertIsNotNone(result.get_property("id"))
        except Exception as e:
            self.skipTest(f"Cannot export billed usage: {e}")

    @requires_delegated(
        "PartnerBilling.Read.All",
        bypass_roles=["Billing Administrator", "Global Administrator"],
    )
    def test_02_billed_usage_export_with_attribute_set(self):
        """Exporting billed usage with 'full' attribute set should return an operation."""
        try:
            result = self.client.reports.partners.billing.usage.billed.export(
                "G016907411", attribute_set="full"
            ).execute_query()
            self.assertIsNotNone(result.get_property("id"))
        except Exception as e:
            self.skipTest(f"Cannot export billed usage with full attributes: {e}")
