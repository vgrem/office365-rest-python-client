import uuid
from typing import Optional

from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamApps(GraphDelegatedTestCase):
    """Tests for team Apps"""

    target_team: Optional[Team] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        team_name = "Team_" + uuid.uuid4().hex
        new_team = cls.client.teams.create(team_name).get().execute_query_retry()
        cls.target_team = new_team

    @classmethod
    def tearDownClass(cls):
        if cls.target_team is not None:
            cls.target_team.delete_object().execute_query_retry()

    @requires_delegated(
        "AppCatalog.Read.All",
        "AppCatalog.ReadWrite.All",
        "Team.ReadBasic.All",
        "Team.Read.All",
        "Team.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test1_list_team_apps(self):
        """Test listing installed apps for a team"""
        assert TestTeamApps.target_team is not None
        result = TestTeamApps.target_team.installed_apps.get().execute_query()
        self.assertIsNotNone(result.resource_path)
