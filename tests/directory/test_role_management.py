from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestRoleManagement(GraphDelegatedTestCase):
    @requires_delegated(
        "EntitlementManagement.Read.All",
        "EntitlementManagement.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test1_list_role_definitions(self):
        """List role definitions"""
        result = self.client.role_management.directory.role_definitions.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("RoleManagement.Read.All", "Directory.Read.All", bypass_roles=["Global Administrator"])
    def test2_get_role_definition(self):
        """Get a role definition by ID"""
        result = (
            self.client.role_management.directory.role_definitions["a0b1b346-4d3e-4e8b-98f8-753987be4970"]
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("RoleManagement.Read.All", "Directory.Read.All", bypass_roles=["Global Administrator"])
    def test3_list_role_assignments(self):
        """List role assignments"""
        col = self.client.role_management.directory.role_assignments.get().execute_query()
        self.assertIsNotNone(col.resource_path)

    @requires_delegated("RoleManagement.Read.All", "Directory.Read.All", bypass_roles=["Global Administrator"])
    def test4_get_user_role_assignments(self):
        """Get role assignments for a user"""
        user = self.client.users.get_by_principal_name(test_user_principal_name).get().execute_query()
        result = (
            self.client.role_management.directory.role_assignments.filter(f"principalId eq '{user.id}'")
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
