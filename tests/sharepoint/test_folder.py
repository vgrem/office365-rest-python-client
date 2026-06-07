from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.changes.collection import ChangeCollection
from office365.sharepoint.folders.folder import Folder

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointFolder(SPTestCase):
    """SharePoint folder operations tests"""

    parent_folder: ClassVar[Optional[Folder]] = None
    input_folder: ClassVar[Optional[Folder]] = None
    output_folder: ClassVar[Optional[Folder]] = None
    deleted_folder_guid: ClassVar[Optional[str]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent_folder = cls.client.web.default_document_library().root_folder

    def test_01_create_folder(self):
        """Create a new folder"""
        self.assertIsNotNone(TestSharePointFolder.parent_folder)
        result = TestSharePointFolder.parent_folder.folders.add(create_unique_name("input")).execute_query()
        self.assertTrue(result.exists)
        TestSharePointFolder.input_folder = result

    def test_02_list_sub_folders(self):
        """List sub-folders"""
        self.assertIsNotNone(TestSharePointFolder.parent_folder)
        result = TestSharePointFolder.parent_folder.folders.get().execute_query()
        self.assertGreater(len(result), 1)
        for child_folder in result:
            self.assertIsNotNone(child_folder.resource_path)

    def test_03_get_folder_by_id(self):
        """Get folder by unique ID"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        self.assertIsNotNone(TestSharePointFolder.input_folder.unique_id)
        folder_id = TestSharePointFolder.input_folder.unique_id
        folder = self.client.web.get_folder_by_id(folder_id).get().execute_query()
        self.assertIsNotNone(folder.resource_path)
        self.assertTrue(folder.exists)

    def test_04_get_by_path(self):
        """Get folder by path"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        self.assertIsNotNone(TestSharePointFolder.input_folder.name)
        self.assertIsNotNone(TestSharePointFolder.parent_folder)
        folder = (
            TestSharePointFolder.parent_folder.folders.get_by_path(TestSharePointFolder.input_folder.name)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(folder.unique_id)

    # def test6_get_by_path_with_props(self):
    #    folder = self.client.web.folders.get_by_path('Shared Documents')
    #    self.client.load(folder, ["Folders"]).execute_query()
    #    self.assertIsNotNone(folder.resource_path)

    def test_05_update_folder_properties(self):
        """Update folder properties"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        list_item = TestSharePointFolder.input_folder.list_item_all_fields
        list_item.set_property("Title", "New folder title").update().execute_query()

    def test_06_upload_file_into_folder(self):
        """Upload a file into the folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        result = TestSharePointFolder.input_folder.upload_file("sample.txt", "Some content goes here...").execute_query()
        self.assertIsNotNone(result.server_relative_url)

    def test_07_list_files(self):
        """List files in the folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        folder = TestSharePointFolder.input_folder
        self.client.load(folder, ["Files"])
        self.client.execute_query()
        self.assertGreater(len(folder.files), 0)
        for file in folder.files:
            self.assertIsNotNone(file.resource_path)

    def test_08_copy_folder(self):
        """Copy folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        self.assertIsNotNone(TestSharePointFolder.parent_folder)
        output_folder = TestSharePointFolder.parent_folder.folders.add(create_unique_name("output")).execute_query()
        folder_to = TestSharePointFolder.input_folder.copy_to(output_folder).execute_query()
        files_to = folder_to.files.get().execute_query()
        self.assertGreater(len(files_to), 0)
        TestSharePointFolder.output_folder = output_folder

    def test_09_rename_folder(self):
        """Rename folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        folder = TestSharePointFolder.input_folder
        new_folder_name = create_unique_name("Renamed_")
        folder = folder.rename(new_folder_name).get().execute_query()
        self.assertEqual(new_folder_name, folder.name)

    def test_10_move_folder(self):
        """Move folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        self.assertIsNotNone(TestSharePointFolder.output_folder)
        folder = TestSharePointFolder.input_folder
        folder_to = folder.move_to(TestSharePointFolder.output_folder).execute_query()
        self.assertIsNotNone(folder_to.server_relative_url)

    def test_11_recycle_folder(self):
        """Recycle folder"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        result = TestSharePointFolder.input_folder.recycle().execute_query()
        self.assertIsNotNone(result.value)
        TestSharePointFolder.deleted_folder_guid = result.value

    def test_12_restore_folder(self):
        """Restore recycled folder"""
        self.assertIsNotNone(TestSharePointFolder.output_folder)
        self.assertIsNotNone(TestSharePointFolder.deleted_folder_guid)
        recycle_item = self.client.web.recycle_bin.get_by_id(TestSharePointFolder.deleted_folder_guid)
        recycle_item.restore().execute_query()

    def test_13_get_folder_changes(self):
        """Get folder change log"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        changes = TestSharePointFolder.input_folder.get_changes().execute_query()
        self.assertIsInstance(changes, ChangeCollection)
        self.assertGreaterEqual(len(changes), 0)

    def test_14_delete_folders(self):
        """Delete input and output folders"""
        self.assertIsNotNone(TestSharePointFolder.input_folder)
        self.assertIsNotNone(TestSharePointFolder.output_folder)
        TestSharePointFolder.input_folder.delete_object()
        TestSharePointFolder.output_folder.delete_object()
