"""Azure AD users — CRUD, extensions, licensing, and role assignments.

Tests cover:
  - Creating a new user
  - Listing users (top N, count)
  - Getting user licenses
  - Listing subscribed SKUs
  - Removing a user license (placeholder)
  - Listing app role assignments
  - Updating a user property
  - Deleting a user
  - Getting user changes via delta query
  - Getting member groups for the current user
  - Creating, getting, and deleting an extension on the current user
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.extensions.open_type import OpenTypeExtension
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.runtime.client_value_collection import ClientValueCollection

from tests import create_unique_name, test_tenant
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphUser(GraphDelegatedTestCase):
    """Azure AD user CRUD, licensing, extensions, and membership queries."""

    test_user: ClassVar[Optional[User]] = None
    test_extension: ClassVar[Optional[OpenTypeExtension]] = None

    @requires_delegated(
        "User.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test_01_create_user(self):
        """Creating a user returns a valid user with an ID."""
        login = create_unique_name("testuser")
        password = create_unique_name("P@ssw0rd")
        profile = UserProfile(f"{login}@{test_tenant}", password)
        new_user = self.client.users.add(profile).execute_query()
        self.assertIsNotNone(new_user.id)
        self.assertEqual(new_user.get_property("userPrincipalName"), f"{login}@{test_tenant}")
        TestGraphUser.test_user = new_user

    @requires_delegated(
        "User.Read.All",
        "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_02_list_users(self):
        """Listing top 1 user returns exactly one result."""
        result = self.client.users.top(1).get().execute_query()
        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "User.Read.All",
        "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_03_get_users_count(self):
        """Getting the user count returns a numeric value."""
        result = self.client.users.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "User.Read.All",
        "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_04_get_user_licenses(self):
        """A user's assignedLicenses property is a ClientValueCollection."""
        user = TestGraphUser.test_user
        if not user:
            self.skipTest("No test user created from previous test")
        user = user.select(["assignedLicenses"]).get().execute_query()
        self.assertIsInstance(user.assigned_licenses, ClientValueCollection)

    @requires_delegated(
        "Organization.Read.All",
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_05_list_subscribed_skus(self):
        """Listing subscribed SKUs returns a valid collection."""
        skus = self.client.subscribed_skus.get().execute_query()
        self.assertIsNotNone(skus.resource_path)

    def test_06_user_remove_license(self):
        """Remove user license (placeholder)."""

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_07_list_app_role_assignments(self):
        """Listing app role assignments for the test user returns a valid collection."""
        user = TestGraphUser.test_user
        if not user:
            self.skipTest("No test user created from previous test")
        result = user.app_role_assignments.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "User.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test_08_update_user(self):
        """Updating a user property (city) persists and is searchable."""
        user = TestGraphUser.test_user
        if not user:
            self.skipTest("No test user created from previous test")
        prop_name = "city"
        prop_val = create_unique_name("city_")
        user.set_property(prop_name, prop_val).update().execute_query()

        result = self.client.users.filter(f"{prop_name} eq '{prop_val}'").get().execute_query()
        self.assertEqual(len(result), 1)

    @requires_delegated(
        "User.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test_09_delete_user(self):
        """Deleting the test user succeeds and clears the reference."""
        user = TestGraphUser.test_user
        if not user:
            self.skipTest("No test user to delete")
        user.delete_object().execute_query()
        TestGraphUser.test_user = None

    @requires_delegated(
        "User.Read.All",
        "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_10_get_user_changes(self):
        """Getting user changes via delta query returns at least one entry."""
        changed_users = self.client.users.delta.get().execute_query()
        self.assertGreater(len(changed_users), 0)

    @requires_delegated(
        "GroupMember.Read.All",
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_11_get_my_member_groups(self):
        """Getting member groups for the current user returns a value."""
        result = self.client.me.get_member_groups().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "User.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_12_create_extension(self):
        """Creating an extension on the current user returns a valid resource."""
        result = self.client.me.add_extension("Com.Contoso.SSN2").execute_query()
        self.assertIsNotNone(result.resource_path)
        TestGraphUser.test_extension = result

    @requires_delegated(
        "User.Read",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_13_get_extension(self):
        """Getting extensions for the current user returns at least one entry."""
        result = self.client.me.extensions.get().execute_query()
        self.assertGreater(len(result), 0)

    @requires_delegated(
        "User.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_14_delete_extension(self):
        """Deleting the extension from the current user succeeds."""
        extension = TestGraphUser.test_extension
        if not extension:
            self.skipTest("No extension created from previous test")
        extension.delete_object().execute_query()

    @classmethod
    def tearDownClass(cls):
        user = cls.test_user
        if user and user.resource_path:
            try:
                user.delete_object().execute_query()
            except Exception:
                pass
        cls.test_user = None
        cls.test_extension = None
