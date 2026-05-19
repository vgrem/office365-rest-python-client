import uuid
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.lists.template_type import ListTemplateType
from office365.runtime.paths.v4.entity import EntityPath
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFolder(GraphDelegatedTestCase):
    """OneDrive test case for a Folder"""

    target_drive: Optional[Drive] = None
    target_folder: Optional[DriveItem] = None
    target_folder_name = "Archive_" + uuid.uuid4().hex

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        lib_name = create_unique_name("Lib")
        lib = cls.client.sites.root.lists.add(lib_name, ListTemplateType.documentLibrary).execute_query()
        cls.target_drive = lib.drive

    @classmethod
    def tearDownClass(cls):
        assert cls.target_drive is not None
        cls.target_drive.list.delete_object().execute_query()

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test1_create_root_folder(self):
        """Create a root folder in the target drive"""
        assert self.target_drive is not None
        folder = self.target_drive.root.create_folder(self.target_folder_name).execute_query()
        self.assertEqual(folder.name, self.target_folder_name)
        TestFolder.target_folder = folder

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test2_create_child_folder(self):
        """Create a child folder inside the target folder"""
        target_folder_name = "2018"
        assert TestFolder.target_folder is not None
        folder = TestFolder.target_folder.create_folder(target_folder_name).execute_query()
        self.assertEqual(folder.name, target_folder_name)

    @requires_delegated(
        "Files.Read",
        "Files.ReadWrite",
        "Files.Read.All",
        "Files.ReadWrite.All",
        "Group.Read.All",
        "Group.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test3_get_folder_by_path(self):
        """Get a folder by its path"""
        assert self.target_drive is not None
        root_folder = self.target_drive.root.get_by_path(self.target_folder_name).get().execute_query()
        folder = root_folder.get_by_path("2018").get().execute_query()
        self.assertEqual(
            folder.resource_path,
            EntityPath(folder.id, self.target_drive.items.resource_path),
        )

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test4_get_folder_permissions(self):
        """Get permissions of the target folder"""
        assert self.target_folder is not None
        result = self.target_folder.permissions.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test5_update_folder(self):
        """Update the target folder"""
        folder = self.target_folder
        assert folder is not None
        folder.update().execute_query()

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test6_get_analytics(self):
        """Get analytics for the target folder"""
        assert self.target_folder is not None
        result = self.target_folder.analytics.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test7_delete_folder(self):
        """Delete the target folder"""
        assert self.target_folder is not None
        self.target_folder.delete_object().execute_query()
