"""Tests for SharePoint team site creation, status, deletion, and group management."""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.portal.sites.status import SiteStatus
from office365.sharepoint.sites.site import Site

from tests import (
    test_client_id,
    test_password,
    test_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestTeamSite(SPTestCase):
    """Test SharePoint team site features."""

    target_site: ClassVar[Optional[Site]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        cls.client = client

    def test_01_can_user_create_group(self):
        """Check if the user can create a group."""
        result = self.client.group_site_manager.can_user_create_group().execute_query()
        self.assertIsNotNone(result.value)

    def test_02_create_site(self):
        """Create a new team site."""
        site_name = f"TeamSite{uuid.uuid4().hex}"
        site = self.client.create_team_site(site_name, "Team Site", True).execute_query()
        self.assertIsNotNone(site.url)
        TestTeamSite.target_site = site

    def test_03_get_site_status(self):
        """Get the status of the created team site."""
        target_site = TestTeamSite.target_site
        if not target_site:
            self.skipTest("No target site from previous test")
        result = self.client.group_site_manager.get_status(target_site).execute_query()
        self.assertIsNotNone(result.value.SiteStatus)
        self.assertEqual(result.value.SiteStatus, SiteStatus.Ready)

    # def test4_get_notebook_url(self):
    #    group_id = self.target_site.group_id
    #    result = self.client.group_site_manager.notebook(group_id).execute_query()
    #    self.assertIsNotNone(result.value)

    # def test5_get_team_channels(self):
    #    group_id = self.target_site.group_id
    #    result = self.client.group_site_manager.get_team_channels(group_id).execute_query()
    #    self.assertIsNotNone(result.value)

    def test_04_delete_site(self):
        """Delete the created team site."""
        target_site = TestTeamSite.target_site
        if not target_site:
            self.skipTest("No target site from previous test")
        target_site.delete_object().execute_query()

    def test_05_get_current_user_joined_teams(self):
        """Get the list of teams the current user has joined."""
        result = self.client.group_site_manager.get_current_user_joined_teams().execute_query()
        self.assertIsNotNone(result.value)

    def test_06_get_group_creation_context(self):
        """Get the group creation context."""
        result = self.client.group_site_manager.get_group_creation_context().execute_query()
        self.assertIsNotNone(result.value)
