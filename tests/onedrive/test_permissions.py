import uuid
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.permissions.permission import Permission
from tests import (
    test_client_credentials,
    test_team_site_url,
    test_user_principal_name_alt,
)
from tests.decorators import requires_app_permission, requires_delegated
from tests.graph_case import GraphApplicationTestCase


class TestPermissions(GraphApplicationTestCase):
    target_drive_item: Optional[DriveItem] = None
    target_permission: Optional[Permission] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        folder_name = "New_" + uuid.uuid4().hex
        cls.target_drive_item = cls.client.sites.root.drive.root.create_folder(folder_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        assert cls.target_drive_item is not None
        item_to_delete = cls.target_drive_item.get().execute_query()
        item_to_delete.delete_object().execute_query()

    @requires_app_permission("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test1_create_anonymous_link(self):
        """Create an anonymous sharing link"""
        assert TestPermissions.target_drive_item is not None
        permission = TestPermissions.target_drive_item.create_link("view", "anonymous").execute_query()
        self.assertIsNotNone(permission.id)
        self.assertIsNotNone(permission.roles[0], "read")

    @requires_app_permission("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test2_create_company_link(self):
        """Create an organization sharing link"""
        assert TestPermissions.target_drive_item is not None
        permission = TestPermissions.target_drive_item.create_link("edit", "organization").execute_query()
        self.assertIsNotNone(permission.id)
        self.assertIsNotNone(permission.roles[0], "write")

    @requires_app_permission("Files.Read.All", "Files.ReadWrite.All", "Sites.Read.All", "Sites.ReadWrite.All")
    def test4_driveitem_list_permissions(self):
        """List permissions for a drive item"""
        assert TestPermissions.target_drive_item is not None
        permissions = TestPermissions.target_drive_item.permissions.get().execute_query()
        self.assertIsNotNone(permissions.resource_path)
        self.assertGreater(len(permissions), 0)

    @requires_app_permission("Files.Read.All", "Files.ReadWrite.All", "Sites.Read.All", "Sites.ReadWrite.All")
    def test5_driveitem_get_permission(self):
        """Get a specific permission for a drive item"""
        assert TestPermissions.target_drive_item is not None
        result = TestPermissions.target_drive_item.permissions.get().top(1).execute_query()
        self.assertEqual(len(result), 1)
        perm_id = result[0].id
        assert perm_id is not None
        assert TestPermissions.target_drive_item is not None
        perm = TestPermissions.target_drive_item.permissions[perm_id].get().execute_query()
        self.assertIsNotNone(perm.resource_path)
        TestPermissions.target_permission = result[0]

    @requires_delegated("Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test6_driveitem_update_permission(self):
        """Update a drive item permission"""
        # perm_to_update = self.__class__.target_permission
        # perm_to_update.roles = ["read"]
        # perm_to_update.update().execute_query()

    @requires_app_permission("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test7_driveitem_delete_permission(self):
        """Delete a drive item permission"""
        perm_to_delete = TestPermissions.target_permission
        assert perm_to_delete is not None
        perm_to_delete.delete_object().execute_query()

    @requires_delegated(
        "Files.Read", "Files.Read.All", "Files.ReadWrite", "Files.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test8_driveitem_grant_access(self):
        """Grant access to a drive item by URL"""
        file_abs_url = f"{test_team_site_url}/Shared Documents/Financial Sample.xlsx"
        permissions = (
            self.client.shares.by_url(file_abs_url)
            .permission.grant(recipients=[test_user_principal_name_alt], or_roles=["read"])
            .execute_query()
        )
        self.assertIsNotNone(permissions.resource_path)

    @requires_delegated("Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test9_create_site_permission(self):
        """Create a permission on the root site"""
        app = self.client.applications.get_by_app_id(test_client_credentials.client_id)
        new_site_permission = self.client.sites.root.permissions.add(["write"], app).execute_query()
        assert new_site_permission.resource_path is not None
        self.target_permission = new_site_permission

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test_10_list_site_permissions(self):
        """List all permissions on the root site"""
        site_permissions = self.client.sites.root.permissions.get().execute_query()
        self.assertIsNotNone(site_permissions.resource_path)

    @requires_delegated("Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test_11_delete_site_permission(self):
        """Delete a site permission"""
        assert self.target_permission is not None
        self.target_permission.delete_object().execute_query()
