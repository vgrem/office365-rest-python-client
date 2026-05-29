import unittest
from typing import Optional

from office365.directory.groups.group import Group
from office365.directory.users.user import User
from office365.runtime.client_request_exception import ClientRequestException

from tests import create_unique_name, test_user_principal_name
from tests.graph_case import GraphDelegatedTestCase


class TestGraphGroup(GraphDelegatedTestCase):
    """Tests for Azure Active Directory (Azure AD) groups"""

    target_group: Optional[Group] = None
    target_user: Optional[User] = None
    directory_quota_exceeded = False

    def test1_create_group(self):
        """Create a Microsoft 365 group"""
        try:
            name = create_unique_name("Group")
            new_group = self.client.groups.create_m365(name).execute_query()
            self.assertIsNotNone(new_group.id)
            TestGraphGroup.target_group = new_group
        except ClientRequestException as e:
            if e.code == "Directory_QuotaExceeded":
                self.directory_quota_exceeded = True
                result = self.client.me.get_member_groups().execute_query()
                self.assertIsNotNone(result.value)
                filter_expr = f"displayName eq '{result.value[0]}'"
                result = self.client.groups.filter(filter_expr).get().execute_query()
                TestGraphGroup.target_group = result[0]

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not be created")
    def test2_list_groups(self):
        """List groups"""
        result = self.client.groups.top(1).get().execute_query()
        self.assertEqual(len(result), 1)

    def test3_get_groups_count(self):
        """Get groups count"""
        result = self.client.groups.count().execute_query()
        self.assertIsNotNone(result.value)

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not be created")
    def test4_get_group(self):
        """Get a group by ID"""
        assert TestGraphGroup.target_group is not None
        existing_group = TestGraphGroup.target_group
        assert existing_group.id is not None
        target_group = self.client.groups[existing_group.id].get().execute_query()
        self.assertIsInstance(target_group, Group)

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not be created")
    def test5_add_group_owner(self):
        """Add an owner to the group"""
        users = self.client.users.filter(f"mail eq '{test_user_principal_name}'").get().execute_query()
        self.assertEqual(len(users), 1)

        owner = users[0]
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.owners.add(owner).execute_query()
        TestGraphGroup.target_user = users[0]

    def test6_list_group_owners(self):
        """List group owners"""
        assert TestGraphGroup.target_group is not None
        owners = TestGraphGroup.target_group.owners.get().execute_query()
        self.assertGreater(len(owners), 0)

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not created")
    def test7_remove_group_owner(self):
        """Remove an owner from the group"""
        assert TestGraphGroup.target_user is not None
        owner_id = TestGraphGroup.target_user.id
        assert owner_id is not None
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.owners.remove(owner_id).execute_query()

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not created")
    def test8_add_group_member(self):
        """Add a member to the group"""
        assert TestGraphGroup.target_user is not None
        member = TestGraphGroup.target_user
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.members.add(member).execute_query()

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not created")
    def test9_remove_group_member(self):
        """Remove a member from the group"""
        assert TestGraphGroup.target_user is not None
        member_id = TestGraphGroup.target_user.id
        assert member_id is not None
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.members.remove(member_id).execute_query()

    @unittest.skipIf(directory_quota_exceeded, "Skipping, group was not created")
    def test_10_delete_group(self):
        """Delete the group"""
        assert TestGraphGroup.target_group is not None
        grp_to_delete = TestGraphGroup.target_group
        grp_to_delete.delete_object(True).execute_query()

    def test_11_get_changes(self):
        """Get group changes via delta query"""
        changed_groups = self.client.groups.delta.select(["displayName"]).get().execute_query()
        self.assertGreater(len(changed_groups), 0)
