from typing import Optional

from office365.directory.administrative_unit import AdministrativeUnit
from office365.runtime.client_value_collection import ClientValueCollection

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDirectory(GraphDelegatedTestCase):
    administrative_unit: Optional[AdministrativeUnit] = None

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test2_get_deleted_groups(self):
        """Get deleted groups"""
        result = self.client.directory.deleted_groups.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.group")

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test3_get_deleted_users(self):
        """Get deleted users"""
        result = self.client.directory.deleted_users.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.user")

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test4_get_deleted_applications(self):
        """Get deleted applications"""
        result = self.client.directory.deleted_applications.get().execute_query()
        self.assertEqual(result.resource_path.segment, "microsoft.graph.application")

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test5_get_member_objects(self):
        """Get member objects for the current user"""
        result = self.client.me.get_member_objects().execute_query()
        self.assertIsInstance(result.value, ClientValueCollection)

    @requires_delegated(
        "RoleManagement.Read.Directory",
        "RoleManagement.Read.All",
        "Directory.Read.All",
        bypass_roles=["Privileged Role Administrator", "Global Administrator", "Global Reader"],
    )
    def test6_list_directory_roles(self):
        """List directory roles"""
        result = self.client.directory_roles.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "AdministrativeUnit.Read.All",
        "AdministrativeUnit.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test8_list_administrative_units(self):
        """List administrative units"""
        result = self.client.directory.administrative_units.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_11_list_directory_role_templates(self):
        """List directory role templates"""
        result = self.client.directory_role_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_12_list_device_local_credentials(self):
        """List device local credentials"""
        result = self.client.directory.device_local_credentials.get().execute_query()
        self.assertIsNotNone(result.resource_path)
