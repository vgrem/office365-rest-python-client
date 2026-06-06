from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.principal.groups.group import Group

from tests import create_unique_name, test_user_principal_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointGroup(SPTestCase):
    """SharePoint group operations tests"""

    result_group: ClassVar[Optional[Group]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_user = cls.client.web.ensure_user(test_user_principal_name).execute_query()

    def test_01_create_group(self):
        """Create a SharePoint group"""
        grp_title = create_unique_name("Custom Group")
        result = self.client.web.site_groups.add(grp_title).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestSharePointGroup.result_group = result

    def test_02_add_user_to_group(self):
        """Add a user to the group"""
        if TestSharePointGroup.result_group is None:
            self.skipTest("Prerequisite failed - no group created")
        self.assertIsNotNone(TestSharePointGroup.result_group)
        result = TestSharePointGroup.result_group.users.add_user(self.target_user.login_name).execute_query()
        self.assertIsNotNone(result.id)

    def test_03_get_group_users(self):
        """Get users in the group"""
        if TestSharePointGroup.result_group is None:
            self.skipTest("Prerequisite failed - no group created")
        self.assertIsNotNone(TestSharePointGroup.result_group)
        result = TestSharePointGroup.result_group.users.get().execute_query()
        self.assertGreaterEqual(len(result), 1)

    def test_04_expand_to_principals(self):
        """Expand group to principals"""
        if TestSharePointGroup.result_group is None:
            self.skipTest("Prerequisite failed - no group created")
        self.assertIsNotNone(TestSharePointGroup.result_group)
        result = TestSharePointGroup.result_group.expand_to_principals().execute_query()
        self.assertIsNotNone(result.value)

    def test_05_remove_user_from_group(self):
        """Remove a user from the group"""
        if TestSharePointGroup.result_group is None:
            self.skipTest("Prerequisite failed - no group created")
        self.assertIsNotNone(TestSharePointGroup.result_group)
        result = TestSharePointGroup.result_group.users.remove_by_id(self.target_user.id).execute_query()
        self.assertEqual(len(result), 0)

    def test_06_delete_group(self):
        """Delete the group"""
        if TestSharePointGroup.result_group is None:
            self.skipTest("Prerequisite failed - no group created")
        self.assertIsNotNone(TestSharePointGroup.result_group)
        grp_id = TestSharePointGroup.result_group.id
        self.client.web.site_groups.remove_by_id(grp_id).execute_query()
