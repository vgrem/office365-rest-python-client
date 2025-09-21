from office365.sharepoint.permissions.base_permissions import BasePermissions
from office365.sharepoint.permissions.kind import PermissionKind
from office365.sharepoint.permissions.roles.definitions.definition import RoleDefinition
from office365.sharepoint.sharing.role_type import RoleType
from tests.sharepoint.sharepoint_case import SPTestCase


class TestRoles(SPTestCase):
    target_role: RoleDefinition = None
    role_name = "Create and Manage Alerts 456"

    def test1_create_role(self):
        permissions = BasePermissions()
        permissions.set(PermissionKind.CreateAlerts)
        permissions.set(PermissionKind.ManageAlerts)
        result = self.client.web.role_definitions.add(
            permissions, self.role_name
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_role = result

    def test2_get_by_type(self):
        result = (
            self.client.web.role_definitions.get_by_type(RoleType.Contributor)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    def test3_get_by_name(self):
        result = (
            self.client.web.role_definitions.get_by_name(self.role_name)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    def test4_add_role_assignment(self):
        target_user = self.client.web.current_user
        result = self.client.web.add_role_assignment(
            target_user, self.target_role
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test5_find_role_assignments(self):
        target_user = self.client.web.current_user.get().execute_query()
        result = self.client.web.role_assignments.filter(f"PrincipalId eq {target_user.id}").get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test6_get_role_assignment(self):
        target_user = self.client.web.current_user
        result = self.client.web.get_role_assignment(target_user).get().execute_query()
        self.assertIsNotNone(result.principal_id)

    def test7_remove_role_assignment(self):
        target_user = self.client.web.current_user
        result = self.client.web.remove_role_assignment(
            target_user, self.target_role
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test8_delete_role(self):
        self.target_role.delete_object().execute_query()
