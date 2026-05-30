from typing import Optional

from office365.directory.groups.group import Group
from office365.directory.users.user import User

from tests import create_unique_name, test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphGroup(GraphDelegatedTestCase):
    """Tests for Azure Active Directory (Azure AD) groups"""

    target_group: Optional[Group] = None
    target_user: Optional[User] = None

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test1_create_group(self):
        """Create a Microsoft 365 group"""
        name = create_unique_name("Group")
        new_group = self.client.groups.create_m365(name).execute_query()
        self.assertIsNotNone(new_group.id)
        TestGraphGroup.target_group = new_group

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test2_list_groups(self):
        """List groups"""
        result = self.client.groups.top(1).get().execute_query()
        self.assertEqual(len(result), 1)

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test3_get_groups_count(self):
        """Get groups count"""
        result = self.client.groups.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test4_get_group(self):
        """Get a group by ID"""
        assert TestGraphGroup.target_group is not None
        existing_group = TestGraphGroup.target_group
        assert existing_group.id is not None
        target_group = self.client.groups[existing_group.id].get().execute_query()
        self.assertIsInstance(target_group, Group)

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test5_add_group_owner(self):
        """Add an owner to the group"""
        users = self.client.users.filter(f"mail eq '{test_user_principal_name}'").get().execute_query()
        self.assertEqual(len(users), 1)

        owner = users[0]
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.owners.add(owner).execute_query()
        TestGraphGroup.target_user = users[0]

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test6_list_group_owners(self):
        """List group owners"""
        assert TestGraphGroup.target_group is not None
        owners = TestGraphGroup.target_group.owners.get().execute_query()
        self.assertGreater(len(owners), 0)

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test7_remove_group_owner(self):
        """Remove an owner from the group"""
        assert TestGraphGroup.target_user is not None
        owner_id = TestGraphGroup.target_user.id
        assert owner_id is not None
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.owners.remove(owner_id).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test8_add_group_member(self):
        """Add a member to the group"""
        assert TestGraphGroup.target_user is not None
        member = TestGraphGroup.target_user
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.members.add(member).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test9_remove_group_member(self):
        """Remove a member from the group"""
        assert TestGraphGroup.target_user is not None
        member_id = TestGraphGroup.target_user.id
        assert member_id is not None
        assert TestGraphGroup.target_group is not None
        grp = TestGraphGroup.target_group
        grp.members.remove(member_id).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_10_delete_group(self):
        """Delete the group"""
        assert TestGraphGroup.target_group is not None
        grp_to_delete = TestGraphGroup.target_group
        grp_to_delete.delete_object(True).execute_query()

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_11_get_changes(self):
        """Get group changes via delta query"""
        changed_groups = self.client.groups.delta.select(["displayName"]).get().execute_query()
        self.assertGreater(len(changed_groups), 0)
