"""Tests for SharePoint user operations including current user, permissions, and user changes."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.principal.users.user import User

from tests import test_tenant
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointUser(SPTestCase):
    """Test SharePoint user features."""

    target_user: ClassVar[Optional[User]] = None

    def test_01_get_current_user(self):
        """Get the current user."""
        user = self.client.web.current_user.get().execute_query()
        self.assertIsNotNone(user.login_name, "Current user was not requested")
        self.assertIsInstance(user.id, int)
        TestSharePointUser.target_user = user

    def test_02_ensure_user(self):
        """Ensure the target user exists."""
        target_user = TestSharePointUser.target_user
        if not target_user:
            self.skipTest("No target user from previous test")
        self.assertIsNotNone(target_user.login_name)
        result_user = self.client.web.ensure_user(target_user.login_name).execute_query()
        self.assertIsNotNone(result_user.user_id)

    def test_03_get_user(self):
        """Get user by login name."""
        target_user = TestSharePointUser.target_user
        if not target_user:
            self.skipTest("No target user from previous test")
        self.assertIsNotNone(target_user.login_name)
        target_user_result = self.client.web.site_users.get_by_login_name(target_user.login_name).get().execute_query()
        self.assertIsNotNone(target_user_result.id)

    def test_04_update_user(self):
        """Update the target user's email."""
        target_user = TestSharePointUser.target_user
        if not target_user:
            self.skipTest("No target user from previous test")
        user_to_update = target_user
        user_to_update.set_property("Email", f"support@{test_tenant}").update().execute_query()

    def test_05_get_user_permissions(self):
        """Get effective permissions for the target user."""
        target_user = TestSharePointUser.target_user
        if not target_user:
            self.skipTest("No target user from previous test")
        self.assertIsNotNone(target_user.login_name)
        perms_result = self.client.web.get_user_effective_permissions(target_user.login_name)
        self.client.execute_query()
        self.assertIsInstance(perms_result.value, BasePermissions)

    def test_06_get_user_changes(self):
        """Get change log for user changes."""
        result = self.client.site.get_changes(ChangeQuery(User=True)).execute_query()
        self.assertGreater(len(result), 0)
        # self.assertEqual(changes.entity_type_name, "Collection(SP.Change)")

    def test_07_list_site_users(self):
        """List site users from the root web."""
        result = self.client.site.root_web.site_users.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.entity_type_name, "Collection(SP.User)")

    # def test8_get_user_directory_info_by_email(self):
    #    result = SharingUtility.get_user_directory_info_by_email(self.client, test_user_principal_name).execute_query()
    #    self.assertIsNotNone(result.value)

    # def test9_get_user_recent_files(self):
    #    result = self.client.web.current_user.get_recent_files().execute_query()
    #    self.assertIsNotNone(result.value)
