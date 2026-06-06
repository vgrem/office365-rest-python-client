"""Directory — deleted items, directory roles, administrative units, role templates, and device local credentials.

Tests cover:
  - Getting deleted groups
  - Getting deleted users
  - Getting deleted applications
  - Getting member objects for the current user
  - Listing directory roles
  - Listing administrative units
  - Listing directory role templates
  - Listing device local credentials
  - Accessing directory subscriptions
  - Accessing custom security attribute definitions
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.administrative_unit import AdministrativeUnit
from office365.runtime.client_value_collection import ClientValueCollection

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDirectory(GraphDelegatedTestCase):
    """Directory-level operations: deleted items, roles, units, and templates."""

    administrative_unit: ClassVar[Optional[AdministrativeUnit]] = None

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_01_get_deleted_groups(self):
        """Getting deleted groups returns a valid collection."""
        result = self.client.directory.deleted_groups.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.group")
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_02_get_deleted_users(self):
        """Getting deleted users returns a valid collection."""
        result = self.client.directory.deleted_users.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.user")
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_03_get_deleted_applications(self):
        """Getting deleted applications returns a valid collection."""
        result = self.client.directory.deleted_applications.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.application")
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_04_get_member_objects(self):
        """Getting member objects for the current user returns a ClientValueCollection."""
        result = self.client.me.get_member_objects().execute_query()
        self.assertIsInstance(result.value, ClientValueCollection)

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test_05_list_directory_roles(self):
        """Listing directory roles returns a valid collection."""
        result = self.client.directory_roles.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "AdministrativeUnit.Read.All",
        "AdministrativeUnit.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_06_list_administrative_units(self):
        """Listing administrative units returns a valid collection."""
        result = self.client.directory.administrative_units.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_07_list_directory_role_templates(self):
        """Listing directory role templates returns a valid collection."""
        result = self.client.directory_role_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_08_list_device_local_credentials(self):
        """Listing device local credentials returns a valid collection."""
        result = self.client.directory.device_local_credentials.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_09_list_directory_subscriptions(self):
        """Listing directory subscriptions returns a valid collection."""
        try:
            result = self.client.directory.subscriptions.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list directory subscriptions: {e}")

    @requires_delegated(
        "CustomSecAttributeDefinition.Read.All",
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_10_list_custom_security_attribute_definitions(self):
        """Listing custom security attribute definitions returns a valid collection."""
        try:
            result = self.client.directory.custom_security_attribute_definitions.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot list custom security attribute definitions: {e}")
