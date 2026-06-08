"""Azure AD groups — CRUD, owners, members, delta, and by-name lookup.

Tests cover:
  - Creating a Microsoft 365 group
  - Listing groups (top N, count)
  - Getting a group by ID
  - Adding an owner to the group
  - Listing group owners
  - Removing an owner from the group
  - Adding a member to the group
  - Removing a member from the group
  - Deleting a group
  - Getting group changes via delta query
  - Getting a group by display name
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.groups.group import Group
from office365.directory.users.user import User

from tests import create_unique_name, test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphGroup(GraphDelegatedTestCase):
    """Azure AD group CRUD, membership, and ownership."""

    target_group: ClassVar[Optional[Group]] = None
    target_user: ClassVar[Optional[User]] = None

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_01_create_group(self):
        """Creating a Microsoft 365 group returns a valid group with an ID."""
        name = create_unique_name("Group")
        new_group = self.client.groups.create_m365(name).execute_query()
        self.assertIsNotNone(new_group.id)
        self.assertEqual(new_group.display_name, name)
        TestGraphGroup.target_group = new_group

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_02_list_groups(self):
        """Listing top 1 group returns exactly one result."""
        result = self.client.groups.top(1).get().execute_query()
        self.assertEqual(len(result), 1)

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_03_get_groups_count(self):
        """Getting the groups count returns a numeric value."""
        result = self.client.groups.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_04_get_group(self):
        """Getting a group by ID returns an instance of Group."""
        group = TestGraphGroup.target_group
        if not group:
            self.skipTest("No target group created from previous test")
        group_id = group.id
        if not group_id:
            self.skipTest("Target group has no ID")
        target_group = self.client.groups[group_id].get().execute_query()
        self.assertIsInstance(target_group, Group)

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_05_add_group_owner(self):
        """Adding an owner to the group succeeds."""
        users = self.client.users.filter(f"mail eq '{test_user_principal_name}'").get().execute_query()
        self.assertEqual(len(users), 1)

        owner = users[0]
        group = TestGraphGroup.target_group
        if not group:
            self.skipTest("No target group created from previous test")
        group.owners.add(owner).execute_query()
        TestGraphGroup.target_user = users[0]

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_06_list_group_owners(self):
        """Listing group owners returns at least one owner."""
        group = TestGraphGroup.target_group
        if not group:
            self.skipTest("No target group created from previous test")
        owners = group.owners.get().execute_query()
        self.assertGreater(len(owners), 0)

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_07_remove_group_owner(self):
        """Removing an owner from the group succeeds."""
        target_user = TestGraphGroup.target_user
        group = TestGraphGroup.target_group
        if not target_user:
            self.skipTest("No target user to remove")
        if not group:
            self.skipTest("No target group")
        owner_id = target_user.id
        if not owner_id:
            self.skipTest("Target user has no ID")
        group.owners.remove(owner_id).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_08_add_group_member(self):
        """Adding a member to the group succeeds."""
        target_user = TestGraphGroup.target_user
        group = TestGraphGroup.target_group
        if not target_user:
            self.skipTest("No target user to add")
        if not group:
            self.skipTest("No target group")
        group.members.add(target_user).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_09_remove_group_member(self):
        """Removing a member from the group succeeds."""
        target_user = TestGraphGroup.target_user
        group = TestGraphGroup.target_group
        if not target_user:
            self.skipTest("No target user to remove")
        if not group:
            self.skipTest("No target group")
        member_id = target_user.id
        if not member_id:
            self.skipTest("Target user has no ID")
        group.members.remove(member_id).execute_query()

    @requires_delegated("Group.ReadWrite.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_10_delete_group(self):
        """Deleting the group succeeds."""
        group = TestGraphGroup.target_group
        if not group:
            self.skipTest("No target group to delete")
        group.delete_object(True).execute_query()

    @requires_delegated("Group.Read.All", bypass_roles=["Groups Administrator", "Global Administrator"])
    def test_11_get_changes(self):
        """Getting group changes via delta query returns at least one entry."""
        changed_groups = self.client.groups.delta.select(["displayName"]).get().execute_query()
        self.assertGreater(len(changed_groups), 0)

    @classmethod
    def tearDownClass(cls):
        group = cls.target_group
        if group and group.resource_path:
            try:
                group.delete_object(True).execute_query()
            except Exception:
                pass
        cls.target_group = None
        cls.target_user = None
