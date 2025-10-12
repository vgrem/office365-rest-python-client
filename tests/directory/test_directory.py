from office365.directory.administrative_unit import AdministrativeUnit
from office365.runtime.client_value_collection import ClientValueCollection
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestDirectory(GraphTestCase):
    administrative_unit: AdministrativeUnit = None

    def test2_get_deleted_groups(self):
        result = self.client.directory.deleted_groups.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.group")

    def test3_get_deleted_users(self):
        result = self.client.directory.deleted_users.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.user")

    def test4_get_deleted_applications(self):
        result = self.client.directory.deleted_applications.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.application")

    def test5_get_member_objects(self):
        result = self.client.me.get_member_objects().execute_query()
        self.assertIsInstance(result.value, ClientValueCollection)

    def test6_list_directory_roles(self):
        result = self.client.directory_roles.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # Privileged Role Administrator is required
    # @requires_delegated_permission("AdministrativeUnit.ReadWrite.All")
    # def test7_create_administrative_unit(self):
    #    name = "Seattle District Technical Schools"
    #    result = self.client.directory.administrative_units.add(
    #        displayName=name
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)
    #    self.__class__.administrative_unit = result

    @requires_delegated_permission(
        "AdministrativeUnit.Read.All",
        "AdministrativeUnit.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
    )
    def test8_list_administrative_units(self):
        result = self.client.directory.administrative_units.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test_10_delete_administrative_unit(self):
    #    self.__class__.administrative_unit.delete_object().execute_query()

    def test_11_list_directory_role_templates(self):
        result = self.client.directory_role_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_12_list_device_local_credentials(self):
        result = self.client.directory.device_local_credentials.get().execute_query()
        self.assertIsNotNone(result.resource_path)
