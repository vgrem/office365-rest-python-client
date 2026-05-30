import uuid
from typing import Optional

from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphTeam(GraphDelegatedTestCase):
    """Tests for teams"""

    target_team: Optional[Team] = None

    @requires_delegated(
        "Team.Create",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test1_create_team(self):
        """Test creating a team"""
        team_name = "Group_" + uuid.uuid4().hex
        result = self.client.teams.create(team_name).execute_query()
        self.assertIsNotNone(result.id)
        TestGraphTeam.target_team = result

    @requires_delegated(
        "Team.ReadBasic.All",
        "TeamSettings.Read.All",
        "TeamSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test3_list_all_teams_in_org(self):
        """Test listing all teams in organization"""
        result = self.client.teams.get_all().execute_query()
        self.assertGreater(len(result), 0)

    @requires_delegated(
        "Team.ReadBasic.All", "Team.Read.All", bypass_roles=["Global Administrator", "Teams Administrator"]
    )
    def test4_list_joined_teams(self):
        """Test listing joined teams"""
        result = self.client.me.joined_teams.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreater(len(result), 0)

    @requires_delegated(
        "Team.ReadBasic.All",
        "TeamSettings.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        "Group.Read.All",
        "Group.ReadWrite.All",
        "TeamSettings.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test5_get_team(self):
        """Test getting a team"""
        assert TestGraphTeam.target_team is not None
        group_id = TestGraphTeam.target_team.id
        assert group_id is not None
        existing_team = self.client.teams[group_id].get().execute_query()
        self.assertIsNotNone(existing_team.resource_path)
        self.assertIsNotNone(existing_team.messaging_settings)

        if existing_team.is_archived:
            existing_team.unarchive()
            self.client.load(existing_team)
            self.client.execute_query()
            self.assertFalse(existing_team.is_archived)

    @requires_delegated(
        "TeamSettings.ReadWrite.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test6_update_team(self):
        """Test updating a team"""
        assert TestGraphTeam.target_team is not None
        team = TestGraphTeam.target_team
        team.fun_settings.allowGiphy = False
        team.update().execute_query()

    @requires_delegated(
        "TeamSettings.ReadWrite.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test7_archive_team(self):
        """Test archiving a team"""
        assert TestGraphTeam.target_team is not None
        team = TestGraphTeam.target_team
        team.archive().execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Global Administrator", "Teams Administrator"])
    def test9_delete_team(self):
        """Test deleting a team"""
        assert TestGraphTeam.target_team is not None
        team_to_delete = TestGraphTeam.target_team
        team_to_delete.delete_object().execute_query_retry()
