import uuid

from office365.teams.team import Team
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestGraphTeam(GraphTestCase):
    """Tests for teams"""

    target_team = None  # type: Team

    @classmethod
    def setUpClass(cls):
        super(TestGraphTeam, cls).setUpClass()

    @requires_delegated_permission(
        "Team.Create", "Directory.ReadWrite.All", "Group.ReadWrite.All"
    )
    def test1_create_team(self):
        team_name = "Group_" + uuid.uuid4().hex
        team = self.client.teams.create(team_name).execute_query()
        self.assertIsNotNone(team.id)
        self.__class__.target_team = team

    @requires_delegated_permission(
        "Team.ReadBasic.All", "TeamSettings.Read.All", "TeamSettings.ReadWrite.All"
    )
    def test3_list_all_teams_in_org(self):
        teams = self.client.teams.get_all().execute_query()
        self.assertGreater(len(teams), 0)

    def test4_list_joined_teams(self):
        my_teams = self.client.me.joined_teams.get().execute_query()
        self.assertIsNotNone(my_teams.resource_path)
        self.assertGreater(len(my_teams), 0)

    @requires_delegated_permission(
        "Team.ReadBasic.All",
        "TeamSettings.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        "Group.Read.All",
        "Group.ReadWrite.All",
        "TeamSettings.Read.All",
    )
    def test5_get_team(self):
        group_id = self.__class__.target_team.id
        existing_team = self.client.teams[group_id].get().execute_query()
        self.assertIsNotNone(existing_team.resource_path)
        self.assertIsNotNone(existing_team.messaging_settings)

        if existing_team.is_archived:
            existing_team.unarchive()
            self.client.load(existing_team)
            self.client.execute_query()
            self.assertFalse(existing_team.is_archived)

    @requires_delegated_permission(
        "TeamSettings.ReadWrite.All", "Directory.ReadWrite.All", "Group.ReadWrite.All"
    )
    def test6_update_team(self):
        team_id = self.__class__.target_team.id
        team_to_update = self.client.teams[team_id]
        team_to_update.fun_settings.allowGiphy = False
        team_to_update.update().execute_query()

    @requires_delegated_permission(
        "TeamSettings.ReadWrite.All", "Directory.ReadWrite.All", "Group.ReadWrite.All"
    )
    def test7_archive_team(self):
        team_id = self.__class__.target_team.id
        self.client.teams[team_id].archive().execute_query()

    @requires_delegated_permission("Group.ReadWrite.All")
    def test8_delete_team(self):
        team_to_delete = self.__class__.target_team
        team_to_delete.delete_object().execute_query_retry()
