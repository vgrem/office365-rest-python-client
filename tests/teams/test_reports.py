from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamsReports(GraphDelegatedTestCase):
    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test1_get_teams_team_counts(self):
        """Test getting teams team counts"""
        result = self.client.reports.get_teams_team_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test2_get_teams_user_activity_counts(self):
        """Test getting teams user activity counts"""
        result = self.client.reports.get_teams_user_activity_user_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Reports.Read.All",
        bypass_roles=["Teams Administrator", "Reports Reader", "Global Administrator", "Global Reader"],
    )
    def test3_get_teams_user_activity_user_counts(self):
        """Test getting teams user activity user counts"""
        result = self.client.reports.get_teams_user_activity_user_counts("D90").execute_query()
        self.assertIsNotNone(result.value)
