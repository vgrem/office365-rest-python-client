from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestTeamsReports(GraphDelegatedTestCase):
    @requires_delegated_permission_or_role("Reports.Read.All", roles=["Global Administrator"])
    def test1_get_teams_team_counts(self):
        """Test getting teams team counts"""
        result = self.client.reports.get_teams_team_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role("Reports.Read.All", roles=["Global Administrator"])
    def test2_get_teams_user_activity_counts(self):
        """Test getting teams user activity counts"""
        result = self.client.reports.get_teams_user_activity_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role("Reports.Read.All", roles=["Global Administrator"])
    def test3_get_teams_user_activity_user_counts(self):
        """Test getting teams user activity user counts"""
        result = self.client.reports.get_teams_user_activity_user_counts("D90").execute_query()
        self.assertIsNotNone(result.value)
