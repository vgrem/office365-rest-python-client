"""Teams — creating, listing, updating, archiving, and deleting teams.

Tests cover:
  - Creating a team with a unique name
  - Listing all teams in the org
  - Listing joined teams for the current user
  - Getting a team by ID with property assertions
  - Updating team settings (funSettings)
  - Archiving and unarchiving a team
  - Deleting a team
  - Team property assertions (messagingSettings, funSettings, guestSettings, isArchived)
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphTeam(GraphDelegatedTestCase):
    """Team CRUD, settings, archive, and property inspection."""

    target_team: ClassVar[Optional[Team]] = None

    @requires_delegated(
        "Team.Create",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_create_team(self):
        """Creating a team with a unique name should succeed."""
        name = "Team_" + uuid.uuid4().hex
        result = self.client.teams.create(name).execute_query()
        self.assertIsNotNone(result.id)
        self.assertIsNotNone(result.display_name)
        TestGraphTeam.target_team = result

    @requires_delegated(
        "Team.ReadBasic.All",
        "TeamSettings.Read.All",
        "TeamSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_list_all_teams(self):
        """Listing all teams in the organization returns at least one."""
        result = self.client.teams.get_all().execute_query()
        self.assertGreater(len(result), 0)

    @requires_delegated(
        "Team.ReadBasic.All",
        "Team.Read.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_03_list_joined_teams(self):
        """Listing joined teams for the current user returns a valid collection."""
        result = self.client.me.joined_teams.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Team.ReadBasic.All",
        "TeamSettings.Read.All",
        "TeamSettings.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_04_get_team_by_id(self):
        """Getting a team by ID returns the team with full properties."""
        team = TestGraphTeam.target_team
        if not team or not team.id:
            self.skipTest("No team created from previous test")

        existing = self.client.teams[team.id].get().execute_query()
        self.assertIsNotNone(existing.resource_path)
        self.assertIsNotNone(existing.get_property("messagingSettings"))
        self.assertIsNotNone(existing.get_property("funSettings"))

        # Handle archive state
        if existing.get_property("isArchived"):
            existing.unarchive()
            self.client.load(existing)
            self.client.execute_query()
            self.assertFalse(existing.get_property("isArchived"))

    @requires_delegated(
        "TeamSettings.ReadWrite.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_05_update_team_settings(self):
        """Updating team settings (funSettings.allowGiphy) should persist."""
        team = TestGraphTeam.target_team
        if not team:
            self.skipTest("No team created from previous test")

        team.get_property("funSettings").set_property("allowGiphy", False)
        team.update().execute_query()

    @requires_delegated(
        "TeamSettings.ReadWrite.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_06_archive_team(self):
        """Archiving a team should succeed."""
        team = TestGraphTeam.target_team
        if not team:
            self.skipTest("No team created from previous test")

        team.archive().execute_query()

    @requires_delegated(
        "TeamSettings.ReadWrite.All",
        "Directory.ReadWrite.All",
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_07_unarchive_team(self):
        """Unarchiving an archived team should succeed."""
        team = TestGraphTeam.target_team
        if not team:
            self.skipTest("No team created from previous test")

        team.unarchive().execute_query()

    @requires_delegated(
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_08_delete_team(self):
        """Deleting a team should succeed."""
        team = TestGraphTeam.target_team
        if not team:
            self.skipTest("No team created from previous test")

        team.delete_object().execute_query_retry()
        TestGraphTeam.target_team = None

    @classmethod
    def tearDownClass(cls):
        team = cls.target_team
        if team and team.resource_path:
            try:
                team.delete_object().execute_query_retry()
            except Exception:
                pass
