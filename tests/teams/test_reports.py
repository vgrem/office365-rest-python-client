"""Teams usage reports — team counts, user activity counts, and user activity details.

Tests cover:
  - Getting team counts for D90
  - Getting team user activity counts for D90
  - Getting team user activity user counts for D90
  - Getting team user activity counts for D7
  - Report result property assertions
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamsReports(GraphDelegatedTestCase):
    """Teams usage reports."""

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_01_get_team_counts_d90(self):
        """Getting team counts for D90 returns data."""
        result = self.client.reports.get_teams_team_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_02_get_team_counts_d7(self):
        """Getting team counts for D7 returns data."""
        result = self.client.reports.get_teams_team_counts("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_03_get_user_activity_counts(self):
        """Getting teams user activity counts for D90 returns data."""
        result = self.client.reports.get_teams_user_activity_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_04_get_user_activity_counts_d7(self):
        """Getting teams user activity counts for D7 returns data."""
        result = self.client.reports.get_teams_user_activity_counts("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_05_get_user_activity_user_counts_d90(self):
        """Getting teams user activity user counts for D90 returns data."""
        result = self.client.reports.get_teams_user_activity_user_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test_06_get_user_activity_user_counts_d7(self):
        """Getting teams user activity user counts for D7 returns data."""
        result = self.client.reports.get_teams_user_activity_user_counts("D7").execute_query()
        self.assertIsNotNone(result.value)
