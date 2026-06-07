"""Tests for SharePoint role definitions, role assignments, and permission management."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.permissions.kind import PermissionKind
from office365.sharepoint.permissions.roles.definitions.definition import RoleDefinition
from office365.sharepoint.sharing.role_type import RoleType

from tests.sharepoint.sharepoint_case import SPTestCase


class TestRoles(SPTestCase):
    """Test SharePoint role definitions and assignments."""

    target_role: ClassVar[Optional[RoleDefinition]] = None
    role_name = "Create and Manage Alerts 456"

    def test_01_create_role(self):
        """Create a new role definition with specific permissions."""
        permissions = BasePermissions()
        permissions.set(PermissionKind.CreateAlerts)
        permissions.set(PermissionKind.ManageAlerts)
        result = self.client.web.role_definitions.add(permissions, self.role_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestRoles.target_role = result

    def test_02_get_by_type(self):
        """Get a role definition by role type."""
        result = self.client.web.role_definitions.get_by_type(RoleType.Contributor).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_03_get_by_name(self):
        """Get a role definition by name."""
        result = self.client.web.role_definitions.get_by_name(self.role_name).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_04_add_role_assignment(self):
        """Add a role assignment for the current user."""
        target_role = TestRoles.target_role
        if not target_role:
            self.skipTest("No target role from previous test")
        target_user = self.client.web.current_user
        result = self.client.web.add_role_assignment(target_user, target_role).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_05_find_role_assignments(self):
        """Find role assignments for the current user."""
        target_user = self.client.web.current_user.get().execute_query()
        result = self.client.web.role_assignments.filter(f"PrincipalId eq {target_user.id}").get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_get_role_assignment(self):
        """Get the role assignment for the current user."""
        target_user = self.client.web.current_user
        result = self.client.web.get_role_assignment(target_user).get().execute_query()
        self.assertIsNotNone(result.principal_id)

    def test_07_remove_role_assignment(self):
        """Remove a role assignment for the current user."""
        target_role = TestRoles.target_role
        if not target_role:
            self.skipTest("No target role from previous test")
        target_user = self.client.web.current_user
        result = self.client.web.remove_role_assignment(target_user, target_role).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_08_delete_role(self):
        """Delete the created role definition."""
        target_role = TestRoles.target_role
        if not target_role:
            self.skipTest("No target role from previous test")
        target_role.delete_object().execute_query()
