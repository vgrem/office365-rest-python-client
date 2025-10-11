from office365.sharepoint.sharing.role_type import RoleType
from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPListPermissions(SPTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_title = create_unique_name("Tasks")
        cls.target_list = cls.client.web.lists.add_tasks(list_title).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_list.delete_object().execute_query()

    def test2_break_role_inheritance(self):
        self.target_list.break_role_inheritance(False).execute_query()
        result = self.target_list.get().select(["HasUniqueRoleAssignments"]).execute_query()
        self.assertTrue(result.has_unique_role_assignments)

    def test5_assign_perms(self):
        result = self.target_list.add_role_assignment(self.client.web.current_user, RoleType.Contributor).execute_query()
        self.assertEqual(len(result.parent_collection), 1)

    def test6_get_user_perms(self):
        target_user = self.client.web.current_user
        result = self.target_list.get_role_assignment(target_user).get().execute_query()
        self.assertIsNotNone(result.principal_id)

    def test7_list_perms(self):
        result = self.target_list.role_assignments.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(1, len(result))
        first = result[0].get().execute_query()
        self.assertIsNotNone(first.resource_path)

    def test8_revoke_perms(self):
        target_role_def = self.client.web.role_definitions.get_by_type(RoleType.Contributor)
        target_user = self.client.web.current_user
        result = self.target_list.remove_role_assignment(target_user, target_role_def).execute_query()

        self.assertEqual(len(result.parent_collection), 0)

    def test9_reset_role_inheritance(self):
        self.target_list.reset_role_inheritance().execute_query()
        result = self.target_list.get().select(["HasUniqueRoleAssignments"]).execute_query()
        self.assertFalse(result.has_unique_role_assignments)
