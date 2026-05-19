from typing import Optional

from office365.directory.administrative_unit import AdministrativeUnit
from office365.runtime.client_value_collection import ClientValueCollection

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDirectory(GraphDelegatedTestCase):
    administrative_unit: Optional[AdministrativeUnit] = None

    def test2_get_deleted_groups(self):
        """Get deleted groups"""
        result = self.client.directory.deleted_groups.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.group")

    def test3_get_deleted_users(self):
        """Get deleted users"""
        result = self.client.directory.deleted_users.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.user")

    def test4_get_deleted_applications(self):
        """Get deleted applications"""
        result = self.client.directory.deleted_applications.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.application")

    def test5_get_member_objects(self):
        """Get member objects for the current user"""
        result = self.client.me.get_member_objects().execute_query()
        self.assertIsInstance(result.value, ClientValueCollection)

    def test6_list_directory_roles(self):
        """List directory roles"""
        result = self.client.directory_roles.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # Privileged Role Administrator is required
    # @requires_delegated("AdministrativeUnit.ReadWrite.All", or_roles=["Global Administrator"])
    # def test7_create_administrative_unit(self):
    #    name = "Seattle District Technical Schools"
    #    result = self.client.directory.administrative_units.add(
    #        displayName=name
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)
    #    self.__class__.administrative_unit = result

    @requires_delegated(
        "AdministrativeUnit.Read.All",
        "AdministrativeUnit.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test8_list_administrative_units(self):
        """List administrative units"""
        result = self.client.directory.administrative_units.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test_10_delete_administrative_unit(self):
    #    self.__class__.administrative_unit.delete_object().execute_query()

    def test_11_list_directory_role_templates(self):
        """List directory role templates"""
        result = self.client.directory_role_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_12_list_device_local_credentials(self):
        """List device local credentials"""
        result = self.client.directory.device_local_credentials.get().execute_query()
        self.assertIsNotNone(result.resource_path)
