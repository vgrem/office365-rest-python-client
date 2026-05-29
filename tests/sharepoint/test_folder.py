from __future__ import annotations

from office365.sharepoint.changes.collection import ChangeCollection
from office365.sharepoint.folders.folder import Folder

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointFolder(SPTestCase):
    parent_folder: Folder | None = None
    input_folder: Folder | None = None
    output_folder: Folder | None = None
    deleted_folder_guid: str | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent_folder = cls.client.web.default_document_library().root_folder

    def test1_create_folder(self):
        assert self.parent_folder is not None
        result = self.parent_folder.folders.add(create_unique_name("input")).execute_query()
        self.assertTrue(result.exists)
        type(self).input_folder = result

    def test2_list_sub_folders(self):
        assert self.parent_folder is not None
        result = self.parent_folder.folders.get().execute_query()
        self.assertGreater(len(result), 1)
        for child_folder in result:
            self.assertIsNotNone(child_folder.resource_path)

    def test4_get_folder_by_id(self):
        assert self.input_folder is not None
        assert self.input_folder.unique_id is not None
        folder_id = self.input_folder.unique_id
        folder = self.client.web.get_folder_by_id(folder_id).get().execute_query()
        self.assertIsNotNone(folder.resource_path)
        self.assertTrue(folder.exists)

    def test5_get_by_path(self):
        assert self.input_folder is not None
        assert self.input_folder.name is not None
        assert self.parent_folder is not None
        folder = self.parent_folder.folders.get_by_path(self.input_folder.name).get().execute_query()
        self.assertIsNotNone(folder.unique_id)

    # def test6_get_by_path_with_props(self):
    #    folder = self.client.web.folders.get_by_path('Shared Documents')
    #    self.client.load(folder, ["Folders"]).execute_query()
    #    self.assertIsNotNone(folder.resource_path)

    def test7_update_folder_properties(self):
        assert self.input_folder is not None
        list_item = self.input_folder.list_item_all_fields
        list_item.set_property("Title", "New folder title").update().execute_query()

    def test8_upload_file_into_folder(self):
        assert self.input_folder is not None
        result = self.input_folder.upload_file("sample.txt", "Some content goes here...").execute_query()
        self.assertIsNotNone(result.server_relative_url)

    def test9_list_files(self):
        assert self.input_folder is not None
        folder = self.input_folder
        self.client.load(folder, ["Files"])
        self.client.execute_query()
        self.assertGreater(len(folder.files), 0)
        for file in folder.files:
            self.assertIsNotNone(file.resource_path)

    def test_10_copy_folder(self):
        assert self.input_folder is not None
        assert self.parent_folder is not None
        output_folder = self.parent_folder.folders.add(create_unique_name("output")).execute_query()
        folder_to = self.input_folder.copy_to(output_folder).execute_query()
        files_to = folder_to.files.get().execute_query()
        self.assertGreater(len(files_to), 0)
        type(self).output_folder = output_folder

    def test_11_rename_folder(self):
        assert self.input_folder is not None
        folder = self.input_folder
        new_folder_name = create_unique_name("Renamed_")
        folder = folder.rename(new_folder_name).get().execute_query()
        self.assertEqual(new_folder_name, folder.name)

    def test_12_move_folder(self):
        assert self.input_folder is not None
        assert self.output_folder is not None
        folder = self.input_folder
        folder_to = folder.move_to(self.output_folder).execute_query()
        self.assertIsNotNone(folder_to.server_relative_url)

    def test_13_recycle_folder(self):
        assert self.input_folder is not None
        result = self.input_folder.recycle().execute_query()
        self.assertIsNotNone(result.value)
        type(self).deleted_folder_guid = result.value

    def test_14_restore_folder(self):
        assert self.output_folder is not None
        assert self.deleted_folder_guid is not None
        recycle_item = self.client.web.recycle_bin.get_by_id(self.deleted_folder_guid)
        recycle_item.restore().execute_query()

    def test_15_get_folder_changes(self):
        assert self.input_folder is not None
        changes = self.input_folder.get_changes().execute_query()
        self.assertIsInstance(changes, ChangeCollection)
        self.assertGreaterEqual(len(changes), 0)

    def test_16_delete_folders(self):
        assert self.input_folder is not None
        assert self.output_folder is not None
        self.input_folder.delete_object()
        self.output_folder.delete_object()
