"""Tests for Microsoft Teams members API."""

import uuid
from typing import Optional

from office365.teams.team import Team
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamMembers(GraphDelegatedTestCase):
    """Tests for team members (add, list, remove)."""

    target_team: Optional[Team] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        team_name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create(team_name).execute_query()
        cls.target_team = team

    @classmethod
    def tearDownClass(cls):
        if cls.target_team is not None:
            cls.target_team.delete_object().execute_query_retry()

    @requires_delegated(
        "TeamMember.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test1_list_members(self):
        """List all members of a team."""
        assert TestTeamMembers.target_team is not None
        members = TestTeamMembers.target_team.members.get().execute_query()
        self.assertIsNotNone(members.resource_path)
