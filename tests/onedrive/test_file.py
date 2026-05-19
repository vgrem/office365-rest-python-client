import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.lists.template_type import ListTemplateType
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFile(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    target_drive: Optional[Drive] = None
    target_file: Optional[DriveItem] = None
    target_folder: Optional[DriveItem] = None

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
    def test1_create_folder(self):
        """Create a folder in the target drive"""
        target_folder_name = "New_" + uuid.uuid4().hex
        assert self.target_drive is not None
        folder = self.target_drive.root.create_folder(target_folder_name).execute_query()
        self.assertEqual(folder.name, target_folder_name)
        TestFile.target_folder = folder

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test2_get_folder_permissions(self):
        """Get permissions of the target folder"""
        assert TestFile.target_folder is not None
        folder_perms = TestFile.target_folder.permissions.get().execute_query()
        self.assertIsNotNone(folder_perms.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test3_upload_file(self):
        """Upload a file to the target drive"""
        file_name = "SharePoint User Guide.docx"
        file_path = f"{os.path.dirname(__file__)}/../data/{file_name}"
        assert self.target_drive is not None
        TestFile.target_file = self.target_drive.root.upload_file(file_path).execute_query()
        assert self.target_file is not None
        assert self.target_file.web_url is not None

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test4_preview_file(self):
        """Get a preview of the target file"""
        assert TestFile.target_file is not None
        result = TestFile.target_file.preview("1").execute_query()
        self.assertIsNotNone(result.value)

    # def test5_validate_permission(self):
    #    self.__class__.target_file.validate_permission().execute_query()

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test6_checkout(self):
        """Check out the target file"""
        assert TestFile.target_file is not None
        TestFile.target_file.checkout().execute_query()
        target_item = TestFile.target_file.get().select(["publication"]).execute_query()
        self.assertEqual(target_item.publication.level, "checkout")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test7_checkin(self):
        """Check in the target file"""
        assert TestFile.target_file is not None
        TestFile.target_file.checkin("").execute_query()
        target_item = TestFile.target_file.get().select(["publication"]).execute_query()
        self.assertEqual(target_item.publication.level, "published")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test8_list_versions(self):
        """List versions of the target file"""
        assert TestFile.target_file is not None
        versions = TestFile.target_file.versions.get().execute_query()
        self.assertGreater(len(versions), 1)

    # def test9_follow(self):
    #    target_item = self.__class__.target_file.follow().execute_query()
    #    self.assertIsNotNone(target_item.resource_path)

    # def test_10_unfollow(self):
    #    target_item = self.__class__.target_file.unfollow().execute_query()
    #    self.assertIsNotNone(target_item.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_11_upload_file_session(self):
        """Upload a file using resumable upload session"""
        file_name = "big_buck_bunny.mp4"
        local_path = f"{os.path.dirname(__file__)}/../data/{file_name}"
        assert self.target_drive is not None
        target_file = self.target_drive.root.resumable_upload(local_path).get().execute_query()
        self.assertIsNotNone(target_file.web_url)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_12_download_file(self):
        """Download the target file content"""
        assert TestFile.target_file is not None
        result = TestFile.target_file.get_content().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_13_convert_file(self):
        """Convert the target file to PDF"""
        assert TestFile.target_file is not None
        result = TestFile.target_file.convert("pdf").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_14_copy_file(self):
        """Copy the target file"""
        file_name = f"Copied_{uuid.uuid4().hex}_SharePoint User Guide.docx"
        assert TestFile.target_file is not None
        result = TestFile.target_file.copy(file_name).execute_query()
        self.assertIsNotNone(result.value)

    # def test_14_move_file(self):
    #    target_folder = self.__class__.target_folder.parentReference
    #
    #    file_name = "Moved_{0}_SharePoint User Guide.docx".format(uuid.uuid4().hex)
    #    result = self.__class__.target_file.move(file_name, target_folder)
    #    self.client.execute_query()
    #    self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_15_get_activities_by_interval(self):
        """Get activities for the target file by time interval"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        assert TestFile.target_file is not None
        result = TestFile.target_file.get_activities_by_interval(start_time, end_time, "day").execute_query()
        self.assertIsNotNone(result)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_16_get_item_analytics(self):
        """Get analytics for the target file"""
        assert TestFile.target_file is not None
        result = TestFile.target_file.analytics.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_17_extract_sensitivity_labels(self):
        """Extract sensitivity labels from the target file"""
        assert TestFile.target_file is not None
        result = TestFile.target_file.extract_sensitivity_labels().execute_query()
        self.assertIsNotNone(result.value)

    # def test_18_set_retention_label(self):
    #    result = self.target_file.set_retention_label("Retention label for Contracts").execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test_19_delete_file(self):
        """Delete files from the target drive"""
        assert self.target_drive is not None
        items = self.target_drive.root.children.top(2).get().execute_query()
        for item in items:
            item.delete_object().execute_query()
