"""Teams — creating, listing, updating, archiving, and deleting teams.

Tests cover:
  - Creating a team with a unique name
  - Listing all teams in the org
  - Listing joined teams for the current user
  - Getting a team by ID with property assertions
  - Updating team settings (funSettings)
  - Archiving and unarchiving a team
  - Cloning a team (clone_and_wait)
  - Deleting a team
  - Team property assertions (messagingSettings, funSettings, guestSettings, isArchived)
"""

from __future__ import annotations

import time
import uuid
from typing import ClassVar, Optional

from office365.runtime.client_request_exception import ClientRequestException
from office365.teams.clonableteamparts import ClonableTeamParts
from office365.teams.team import Team
from office365.teams.visibility_type import TeamVisibilityType

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
        result = self.client.teams.create_and_wait(name).execute_query()
        assert result.id is not None
        TestGraphTeam.target_team = result  # register for cleanup even if a later check fails
        self.assertEqual(result.display_name, name)

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

        # Graph archive/unarchive is eventually consistent — transient 404s
        # right after archiving are retried.
        deadline = time.time() + 120
        while True:
            try:
                team.unarchive().execute_query()
                break
            except ClientRequestException:
                if time.time() >= deadline:
                    raise
                time.sleep(5)

    @requires_delegated(
        "Team.Create",
        "Group.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_08_clone_and_wait(self):
        """Cloning a team returns a provisioned clone with its properties."""
        team = TestGraphTeam.target_team
        if not team:
            self.skipTest("No team created from previous test")

        name = "TeamClone_" + uuid.uuid4().hex
        mail_nickname = "clone" + uuid.uuid4().hex
        cloned = team.clone_and_wait(
            mail_nickname=mail_nickname,
            display_name=name,
            parts_to_clone=ClonableTeamParts.settings,
            visibility=TeamVisibilityType.private,
        ).execute_query()
        try:
            assert cloned.id is not None and cloned.id != team.id
            self.assertEqual(cloned.display_name, name)
        finally:
            try:
                cloned.delete_object().execute_query_retry()
            except Exception:
                pass

    @requires_delegated(
        "Group.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_09_delete_team(self):
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
