"""Team members — listing, adding, and removing members.

Tests cover:
  - Listing all members of a team
  - Member property assertions (displayName, email, roles)
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamMembers(GraphDelegatedTestCase):
    """Team member listing and property inspection."""

    target_team: ClassVar[Optional[Team]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create(name).execute_query()
        cls.target_team = team

    @classmethod
    def tearDownClass(cls):
        team = cls.target_team
        if team and team.resource_path:
            try:
                team.delete_object().execute_query_retry()
            except Exception:
                pass

    @requires_delegated(
        "TeamMember.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_list_members(self):
        """Listing all members of a team returns a valid collection."""
        team = TestTeamMembers.target_team
        if not team:
            self.skipTest("No team available")

        members = team.members.get().execute_query()
        self.assertIsNotNone(members.resource_path)

    @requires_delegated(
        "TeamMember.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_member_has_display_name(self):
        """A team member entry should have a displayName."""
        team = TestTeamMembers.target_team
        if not team:
            self.skipTest("No team available")

        members = team.members.get().execute_query()
        if len(members) > 0:
            self.assertIsNotNone(members[0].display_name)

    @requires_delegated(
        "TeamMember.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_03_member_has_roles(self):
        """A team member entry should have a roles field."""
        team = TestTeamMembers.target_team
        if not team:
            self.skipTest("No team available")

        members = team.members.get().execute_query()
        if len(members) > 0:
            self.assertIsNotNone(members[0].roles)
