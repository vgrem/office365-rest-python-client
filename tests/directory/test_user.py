from typing import Optional

from office365.directory.extensions.open_type import OpenTypeExtension
from office365.directory.users.profile import UserProfile
from office365.directory.users.user import User
from office365.runtime.client_value_collection import ClientValueCollection

from tests import create_unique_name, test_tenant
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestGraphUser(GraphDelegatedTestCase):
    """Tests for Azure Active Directory (Azure AD) users"""

    test_user: Optional[User] = None
    test_extension: Optional[OpenTypeExtension] = None

    @requires_delegated(
        "User.ReadWrite.All", "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test1_create_user(self):
        """Create a user"""
        login = create_unique_name("testuser")
        password = create_unique_name("P@ssw0rd")
        profile = UserProfile(f"{login}@{test_tenant}", password)
        new_user = self.client.users.add(profile).execute_query()
        self.assertIsNotNone(new_user.id)
        TestGraphUser.test_user = new_user

    @requires_delegated(
        "User.Read.All", "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test2_list_users(self):
        """List users"""
        result = self.client.users.top(1).get().execute_query()
        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "User.Read.All", "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test3_get_users_count(self):
        """Get users count"""
        result = self.client.users.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "User.Read.All", "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test4_get_user_licences(self):
        """Get user licenses"""
        assert TestGraphUser.test_user is not None
        user = TestGraphUser.test_user.select(["assignedLicenses"]).get().execute_query()
        self.assertIsInstance(user.assigned_licenses, ClientValueCollection)

    @requires_delegated(
        "Organization.Read.All", "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test5_list_subscribed_skus(self):
        """List subscribed SKUs"""
        skus = self.client.subscribed_skus.get().execute_query()
        self.assertIsNotNone(skus.resource_path)

    def test6_user_remove_license(self):
        """Remove user license (placeholder)"""

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test7_list_app_role_assignments(self):
        """List app role assignments for the test user"""
        assert TestGraphUser.test_user is not None
        result = TestGraphUser.test_user.app_role_assignments.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "User.ReadWrite.All", "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test8_update_user(self):
        """Update a user property"""
        assert TestGraphUser.test_user is not None
        user_to_update = TestGraphUser.test_user
        prop_name = "city"
        prop_val = create_unique_name("city_")
        user_to_update.set_property(prop_name, prop_val).update().execute_query()

        result = self.client.users.filter(f"{prop_name} eq '{prop_val}'").get().execute_query()
        self.assertEqual(1, len(result))

    @requires_delegated(
        "User.ReadWrite.All", "Directory.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Administrator"],
    )
    def test_10_delete_user(self):
        """Delete the test user"""
        user_to_delete = TestGraphUser.test_user
        if user_to_delete is None:
            self.skipTest("No test user to delete")
        user_to_delete.delete_object().execute_query()
        TestGraphUser.test_user = None

    @requires_delegated(
        "User.Read.All", "Directory.Read.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_11_get_user_changes(self):
        """Get user changes via delta query"""
        changed_users = self.client.users.delta.get().execute_query()
        self.assertGreater(len(changed_users), 0)

    @requires_delegated(
        "GroupMember.Read.All", "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_12_get_my_member_groups(self):
        """Get member groups for the current user"""
        result = self.client.me.get_member_groups().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "User.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_13_create_extension(self):
        """Create an extension for the current user"""
        result = self.client.me.add_extension("Com.Contoso.SSN2").execute_query()
        self.assertIsNotNone(result.resource_path)
        TestGraphUser.test_extension = result

    @requires_delegated(
        "User.Read",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_14_get_extension(self):
        """Get extensions for the current user"""
        result = self.client.me.extensions.get().execute_query()
        self.assertGreater(len(result), 0)

    @requires_delegated(
        "User.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_15_delete_extension(self):
        """Delete the extension"""
        assert TestGraphUser.test_extension is not None
        result = TestGraphUser.test_extension.delete_object().execute_query()
        self.assertIsNotNone(result.resource_path)
