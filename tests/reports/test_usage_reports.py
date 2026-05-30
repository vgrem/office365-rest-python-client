"""Tests for Microsoft Graph Usage Reports API."""

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestUsageReports(GraphDelegatedTestCase):
    """Tests for Microsoft Graph usage reports."""

    @requires_delegated("PartnerBilling.Read.All", bypass_roles=["Global Administrator"])
    def test1_billed_usage_export(self):
        """Export billed usage data."""
        result = self.client.reports.partners.billing.usage.billed.export("G016907411").execute_query()
        self.assertIsNotNone(result.value)
