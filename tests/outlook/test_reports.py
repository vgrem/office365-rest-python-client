"""Outlook & M365 usage reports — email activity, mailbox usage, M365 app usage.

Tests cover:
  - Getting email activity counts for various periods
  - Getting email activity user detail
  - Getting mailbox usage storage
  - Getting mailbox usage mailbox counts
  - Getting M365 app user counts
  - Getting email app usage user counts
  - Edge cases: different period values (D7, D30, D90)
  - Property assertions on report results
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookReports(GraphDelegatedTestCase):
    """Usage reports for email, mailbox, and M365 apps."""

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_get_email_activity_counts(self):
        """Getting email activity counts for D90 returns data."""
        result = self.client.reports.get_email_activity_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_get_email_activity_counts_d7(self):
        """Getting email activity counts for D7 returns data."""
        result = self.client.reports.get_email_activity_counts("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_get_email_activity_counts_d30(self):
        """Getting email activity counts for D30 returns data."""
        result = self.client.reports.get_email_activity_counts("D30").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_get_email_activity_user_detail(self):
        """Getting email activity user details for D7 returns data."""
        result = self.client.reports.get_email_activity_user_detail("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_get_mailbox_usage_storage(self):
        """Getting mailbox usage storage for D30 returns data."""
        result = self.client.reports.get_mailbox_usage_storage("D30").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_get_mailbox_usage_mailbox_counts(self):
        """Getting mailbox usage mailbox counts for D90 returns data."""
        result = self.client.reports.get_mailbox_usage_mailbox_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_get_m365_app_user_counts(self):
        """Getting M365 app user counts returns data."""
        result = self.client.reports.get_m365_app_user_counts().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_08_get_m365_app_user_counts_d7(self):
        """Getting M365 app user counts for D7 returns data."""
        result = self.client.reports.get_m365_app_user_counts("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_09_get_mailbox_usage_detail(self):
        """Getting mailbox usage detail for D7 returns data."""
        result = self.client.reports.get_mailbox_usage_detail("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_10_get_email_app_usage_user_counts(self):
        """Getting email app usage user counts for D7 returns data."""
        result = self.client.reports.get_email_app_usage_user_counts("D7").execute_query()
        self.assertIsNotNone(result.value)
