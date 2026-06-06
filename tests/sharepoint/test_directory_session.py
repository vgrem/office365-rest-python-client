"""Tests for SharePoint directory session operations (user, groups, site availability)."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.directory.session import DirectorySession

from tests import (
    test_client_id,
    test_password,
    test_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestDirectorySession(SPTestCase):
    """Tests for SharePoint directory session operations."""

    client: ClassVar[Optional[ClientContext]] = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = ClientContext(test_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        cls.client = client  # type: ignore[assignment]

    def test_01_init_session(self):
        """Initialize a directory session."""
        target = TestDirectorySession.client
        if not target:
            self.skipTest("No resource from previous test")
        session = target.directory_session.get().execute_query()
        self.assertIsInstance(session, DirectorySession)

    def test_02_get_me(self):
        """Get the current user's directory profile."""
        target = TestDirectorySession.client
        if not target:
            self.skipTest("No resource from previous test")
        me = target.directory_session.me.get().execute_query()
        self.assertIsNotNone(me.resource_path)

    def test_03_get_my_groups(self):
        """Get groups the current user belongs to."""
        target = TestDirectorySession.client
        if not target:
            self.skipTest("No resource from previous test")
        result = target.directory_session.me.get_my_groups().execute_query()
        self.assertIsNotNone(result)
        # self.assertGreater(len(result.value), 0)

    # def test_4_user_member_of(self):
    #    result = self.session.me.is_member_of("").execute_query()
    #    self.assertIsNotNone(result.value)

    def test_04_check_site_availability(self):
        """Check whether the site URL is available."""
        target = TestDirectorySession.client
        if not target:
            self.skipTest("No resource from previous test")
        result = target.directory_provider.check_site_availability(test_site_url).execute_query()
        self.assertIsNotNone(result.value)

    # def test_6_get_graph_user(self):
    #    result = self.client.directory_session.get_graph_user(test_user_principal_name).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test_7_get_directory_provider(self):
    #    from office365.sharepoint.directory.provider.object_data import DirectoryObjectData
    #    data = DirectoryObjectData(id_="75c593b5-e5d2-48f3-b787-6646444b8885")
    #    result = self.client.directory_provider.read_directory_object(data).execute_query()
    #    self.assertIsNotNone(result.resource_path)
