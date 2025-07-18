import uuid

from office365.teams.team import Team
from tests.graph_case import GraphTestCase


class TestTeamApps(GraphTestCase):
    """Tests for team Apps"""

    target_team: Team = None

    @classmethod
    def setUpClass(cls):
        super(TestTeamApps, cls).setUpClass()
        team_name = "Team_" + uuid.uuid4().hex
        new_team = cls.client.teams.create(team_name).get().execute_query_retry()
        cls.target_team = new_team

    @classmethod
    def tearDownClass(cls):
        cls.target_team.delete_object().execute_query_retry()

    def test1_list_team_apps(self):
        result = self.__class__.target_team.installed_apps.get().execute_query()
        self.assertIsNotNone(result.resource_path)
