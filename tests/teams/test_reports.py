from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestTeamsReports(GraphTestCase):
    @requires_delegated_permission("Reports.Read.All")
    def test1_get_teams_team_counts(self):
        result = self.client.reports.get_teams_team_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("Reports.Read.All")
    def test2_get_teams_user_activity_counts(self):
        result = self.client.reports.get_teams_user_activity_counts(
            "D90"
        ).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("Reports.Read.All")
    def test3_get_teams_user_activity_user_counts(self):
        result = self.client.reports.get_teams_user_activity_user_counts(
            "D90"
        ).execute_query()
        self.assertIsNotNone(result.value)
