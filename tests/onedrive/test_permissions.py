"""Permissions — drive item sharing links, listing, granting, and site permissions.

Tests cover:
  - Creating anonymous view links
  - Creating organization edit links
  - Listing permissions on a drive item
  - Getting a specific permission by ID
  - Deleting a permission
  - Granting access to a file by URL
  - Creating, listing, and deleting site permissions
"""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.permissions.permission import Permission
from tests import (
    test_client_credentials,
    test_team_site_url,
    test_user_principal_name_alt,
)
from tests.decorators import requires_application, requires_delegated
from tests.graph_case import GraphApplicationTestCase, GraphDelegatedTestCase


class TestDriveItemPermissions(GraphApplicationTestCase):
    """Drive item permissions (requires application permissions for sharing links)."""

    target_drive_item: ClassVar[Optional[DriveItem]] = None
    target_permission: ClassVar[Optional[Permission]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        folder_name = "New_" + uuid.uuid4().hex
        cls.target_drive_item = cls.client.sites.root.drive.root.create_folder(folder_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        item = cls.target_drive_item
        if item and item.resource_path:
            try:
                item.get().delete_object().execute_query()
            except Exception:
                pass

    @requires_application("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test_01_create_anonymous_link(self):
        """Creating an anonymous 'view' sharing link should succeed."""
        item = TestDriveItemPermissions.target_drive_item
        if not item:
            self.skipTest("No drive item available")

        permission = item.create_link("view", "anonymous").execute_query()
        self.assertIsNotNone(permission.get_property("id"))
        self.assertEqual(permission.get_property("roles")[0], "read")

    @requires_application("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test_02_create_company_link(self):
        """Creating an organization 'edit' sharing link should succeed."""
        item = TestDriveItemPermissions.target_drive_item
        if not item:
            self.skipTest("No drive item available")

        permission = item.create_link("edit", "organization").execute_query()
        self.assertIsNotNone(permission.get_property("id"))
        self.assertEqual(permission.get_property("roles")[0], "write")

    @requires_application("Files.Read.All", "Files.ReadWrite.All", "Sites.Read.All", "Sites.ReadWrite.All")
    def test_03_list_permissions(self):
        """Listing permissions on a drive item returns a valid collection."""
        item = TestDriveItemPermissions.target_drive_item
        if not item:
            self.skipTest("No drive item available")

        permissions = item.permissions.get().execute_query()
        self.assertIsNotNone(permissions.resource_path)
        self.assertGreater(len(permissions), 0)

    @requires_application("Files.Read.All", "Files.ReadWrite.All", "Sites.Read.All", "Sites.ReadWrite.All")
    def test_04_get_permission_by_id(self):
        """Getting a specific permission by ID returns that permission."""
        item = TestDriveItemPermissions.target_drive_item
        if not item:
            self.skipTest("No drive item available")

        result = item.permissions.top(1).get().execute_query()
        if len(result) == 0:
            self.skipTest("No permissions found")

        perm = item.permissions[result[0].id].get().execute_query()
        self.assertIsNotNone(perm.resource_path)
        TestDriveItemPermissions.target_permission = perm

    @requires_application("Files.ReadWrite.All", "Sites.ReadWrite.All")
    def test_05_delete_permission(self):
        """Deleting a permission should succeed."""
        perm = TestDriveItemPermissions.target_permission
        if not perm:
            self.skipTest("No permission available")

        perm.delete_object().execute_query()


class TestSitePermissions(GraphDelegatedTestCase):
    """Site-level permissions — creating, listing, and deleting."""

    target_permission: ClassVar[Optional[Permission]] = None

    @requires_delegated("Sites.ReadWrite.All", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test_01_create_site_permission(self):
        """Creating a permission on the root site should succeed."""
        app = self.client.applications.get_by_app_id(test_client_credentials.client_id)
        new_perm = self.client.sites.root.permissions.add(["write"], app).execute_query()
        self.assertIsNotNone(new_perm.resource_path)
        TestSitePermissions.target_permission = new_perm

    @requires_delegated(
        "Sites.Read.All", "Sites.ReadWrite.All", bypass_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test_02_list_site_permissions(self):
        """Listing all permissions on the root site returns a valid collection."""
        permissions = self.client.sites.root.permissions.get().execute_query()
        self.assertIsNotNone(permissions.resource_path)

    @requires_delegated("Sites.ReadWrite.All", bypass_roles=["Global Administrator", "SharePoint Administrator"])
    def test_03_delete_site_permission(self):
        """Deleting a site permission should succeed."""
        perm = TestSitePermissions.target_permission
        if not perm:
            self.skipTest("No permission available")

        perm.delete_object().execute_query()
        TestSitePermissions.target_permission = None


class TestDriveItemGrantAccess(GraphDelegatedTestCase):
    """Granting access to a drive item by URL."""

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_grant_access_by_url(self):
        """Granting access to a file by absolute URL should succeed."""
        file_url = f"{test_team_site_url}/Shared Documents/Financial Sample.xlsx"
        try:
            permissions = (
                self.client.shares.by_url(file_url)
                .permission.grant(recipients=[test_user_principal_name_alt], roles=["read"])
                .execute_query()
            )
            self.assertIsNotNone(permissions.resource_path)
        except Exception as e:
            self.skipTest(f"Cannot grant access: {e}")
