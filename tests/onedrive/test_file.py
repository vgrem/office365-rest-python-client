import os
import uuid
from datetime import datetime, timedelta

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.graph_case import GraphTestCase


class TestFile(GraphTestCase):
    """OneDrive specific test case base class"""

    target_drive: Drive = None
    target_file: DriveItem = None
    target_folder: DriveItem = None

    @classmethod
    def setUpClass(cls):
        super(TestFile, cls).setUpClass()
        lib_name = create_unique_name("Lib")
        lib = cls.client.sites.root.lists.add(lib_name, ListTemplateType.documentLibrary).execute_query()
        cls.target_drive = lib.drive

    @classmethod
    def tearDownClass(cls):
        cls.target_drive.list.delete_object().execute_query()

    def test1_create_folder(self):
        target_folder_name = "New_" + uuid.uuid4().hex
        folder = self.target_drive.root.create_folder(target_folder_name).execute_query()
        self.assertEqual(folder.name, target_folder_name)
        self.__class__.target_folder = folder

    def test2_get_folder_permissions(self):
        folder_perms = self.__class__.target_folder.permissions.get().execute_query()
        self.assertIsNotNone(folder_perms.resource_path)

    def test3_upload_file(self):
        file_name = "SharePoint User Guide.docx"
        file_path = f"{os.path.dirname(__file__)}/../data/{file_name}"
        self.__class__.target_file = self.target_drive.root.upload_file(file_path).execute_query()
        self.assertIsNotNone(self.target_file.web_url)

    def test4_preview_file(self):
        result = self.__class__.target_file.preview("1").execute_query()
        self.assertIsNotNone(result.value)

    # def test5_validate_permission(self):
    #    self.__class__.target_file.validate_permission().execute_query()

    def test6_checkout(self):
        self.__class__.target_file.checkout().execute_query()
        target_item = self.__class__.target_file.get().select(["publication"]).execute_query()
        self.assertEqual(target_item.publication.level, "checkout")

    def test7_checkin(self):
        self.__class__.target_file.checkin("").execute_query()
        target_item = self.__class__.target_file.get().select(["publication"]).execute_query()
        self.assertEqual(target_item.publication.level, "published")

    def test8_list_versions(self):
        versions = self.__class__.target_file.versions.get().execute_query()
        self.assertGreater(len(versions), 1)

    # def test9_follow(self):
    #    target_item = self.__class__.target_file.follow().execute_query()
    #    self.assertIsNotNone(target_item.resource_path)

    # def test_10_unfollow(self):
    #    target_item = self.__class__.target_file.unfollow().execute_query()
    #    self.assertIsNotNone(target_item.resource_path)

    def test_11_upload_file_session(self):
        file_name = "big_buck_bunny.mp4"
        local_path = f"{os.path.dirname(__file__)}/../data/{file_name}"
        target_file = self.target_drive.root.resumable_upload(local_path).get().execute_query()
        self.assertIsNotNone(target_file.web_url)

    def test_12_download_file(self):
        result = self.__class__.target_file.get_content().execute_query()
        self.assertIsNotNone(result.value)

    def test_13_convert_file(self):
        result = self.__class__.target_file.convert("pdf").execute_query()
        self.assertIsNotNone(result.value)

    def test_14_copy_file(self):
        file_name = f"Copied_{uuid.uuid4().hex}_SharePoint User Guide.docx"
        result = self.__class__.target_file.copy(file_name).execute_query()
        self.assertIsNotNone(result.value)

    # def test_14_move_file(self):
    #    target_folder = self.__class__.target_folder.parentReference

    #    file_name = "Moved_{0}_SharePoint User Guide.docx".format(uuid.uuid4().hex)
    #    result = self.__class__.target_file.move(file_name, target_folder)
    #    self.client.execute_query()
    #    self.assertIsNotNone(result.value)

    def test_15_get_activities_by_interval(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        result = self.__class__.target_file.get_activities_by_interval(start_time, end_time, "day").execute_query()
        self.assertIsNotNone(result)

    def test_16_get_item_analytics(self):
        result = self.__class__.target_file.analytics.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_17_extract_sensitivity_labels(self):
        result = self.__class__.target_file.extract_sensitivity_labels().execute_query()
        self.assertIsNotNone(result.value)

    # def test_18_set_retention_label(self):
    #    result = self.target_file.set_retention_label("Retention label for Contracts").execute_query()
    #    self.assertIsNotNone(result.resource_path)

    def test_19_delete_file(self):
        items = self.target_drive.root.children.top(2).get().execute_query()
        for item in items:
            item.delete_object().execute_query()
