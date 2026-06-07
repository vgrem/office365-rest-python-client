"""Role management — role definitions, assignments, and user-specific queries.

Tests cover:
  - Listing unified role definitions for the directory provider
  - Getting a role definition by ID
  - Listing role assignments
  - Getting role assignments for a specific user
"""

from __future__ import annotations

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestRoleManagement(GraphDelegatedTestCase):
    """Directory role management — definitions, assignments, and user lookups."""

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test_01_list_role_definitions(self):
        """Listing unified role definitions returns a valid collection."""
        result = self.client.role_management.directory.role_definitions.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test_02_get_role_definition(self):
        """Getting a role definition by ID returns a valid resource."""
        role_id = "a0b1b346-4d3e-4e8b-98f8-753987be4970"
        result = self.client.role_management.directory.role_definitions[role_id].get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test_03_list_role_assignments(self):
        """Listing role assignments returns a valid collection."""
        col = self.client.role_management.directory.role_assignments.get().execute_query()
        self.assertIsNotNone(col.resource_path)

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test_04_get_user_role_assignments(self):
        """Getting role assignments for a user returns a valid collection."""
        user = self.client.users.get_by_principal_name(test_user_principal_name).get().execute_query()
        result = (
            self.client.role_management.directory.role_assignments.filter(f"principalId eq '{user.id}'")
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
