"""Team Apps — listing installed apps in a team.

Tests cover:
  - Listing installed apps in a team
  - App property assertions
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.teams.team import Team

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestTeamApps(GraphDelegatedTestCase):
    """Team apps — listing and inspecting installed apps."""

    target_team: ClassVar[Optional[Team]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        name = "Team_" + uuid.uuid4().hex
        team = cls.client.teams.create(name).get().execute_query_retry()
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
        "AppCatalog.Read.All",
        "AppCatalog.ReadWrite.All",
        "Team.ReadBasic.All",
        "Team.Read.All",
        "Team.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_01_list_installed_apps(self):
        """Listing installed apps in a team returns a valid collection."""
        team = TestTeamApps.target_team
        if not team:
            self.skipTest("No team available")

        result = team.installed_apps.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "AppCatalog.Read.All",
        "AppCatalog.ReadWrite.All",
        "Team.ReadBasic.All",
        "Team.Read.All",
        "Team.ReadWrite.All",
        bypass_roles=["Global Administrator", "Teams Administrator"],
    )
    def test_02_installed_app_has_id(self):
        """An installed app entry should have an id."""
        team = TestTeamApps.target_team
        if not team:
            self.skipTest("No team available")

        result = team.installed_apps.get().execute_query()
        if len(result) > 0:
            self.assertIsNotNone(result[0].get_property("id"))
