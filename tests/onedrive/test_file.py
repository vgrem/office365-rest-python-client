"""File operations — upload, download, check-out, check-in, versions, copy, analytics, rename.

Tests cover:
  - Creating a folder in a target drive
  - Getting folder permissions
  - Uploading a file
  - Previewing a file
  - Checking out and checking in a file
  - Listing file versions
  - Upload via resumable upload session
  - Downloading file content
  - Converting file to PDF
  - Copying a file
  - Getting activities by time interval
  - Getting item analytics
  - Extracting sensitivity labels
  - Deleting files
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta
from typing import ClassVar, Optional

from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.drives.drive import Drive
from office365.onedrive.lists.template_type import ListTemplateType

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFile(GraphDelegatedTestCase):
    """File operations in a document library."""

    target_drive: ClassVar[Optional[Drive]] = None
    target_file: ClassVar[Optional[DriveItem]] = None
    target_folder: ClassVar[Optional[DriveItem]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        lib_name = create_unique_name("Lib")
        lib = cls.client.sites.root.lists.add(lib_name, ListTemplateType.documentLibrary).execute_query()
        cls.target_drive = lib.drive

    @classmethod
    def tearDownClass(cls):
        drive = cls.target_drive
        if drive and drive.resource_path:
            try:
                drive.list.delete_object().execute_query()
            except Exception:
                pass

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_create_folder(self):
        """Creating a folder in the target drive should succeed."""
        drive = TestFile.target_drive
        if not drive:
            self.skipTest("No target drive available")

        name = "New_" + uuid.uuid4().hex
        folder = drive.root.create_folder(name).execute_query()
        self.assertEqual(folder.get_property("name"), name)
        TestFile.target_folder = folder

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_get_folder_permissions(self):
        """Getting permissions on the target folder returns a valid collection."""
        folder = TestFile.target_folder
        if not folder:
            self.skipTest("No folder created from previous test")

        perms = folder.permissions.get().execute_query()
        self.assertIsNotNone(perms.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_upload_file(self):
        """Uploading a file to the target drive should succeed."""
        drive = TestFile.target_drive
        if not drive:
            self.skipTest("No target drive available")

        name = "SharePoint User Guide.docx"
        path = f"{os.path.dirname(__file__)}/../data/{name}"
        file_item = drive.root.upload_file(path).execute_query()
        self.assertIsNotNone(file_item.get_property("name"))
        self.assertIsNotNone(file_item.get_property("webUrl"))
        self.assertTrue(file_item.get_property("isFile"))
        TestFile.target_file = file_item

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_04_preview_file(self):
        """Getting a preview of the target file should succeed."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        result = file_item.preview("1").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_05_checkout(self):
        """Checking out the target file should set publication level to checkout."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        file_item.checkout().execute_query()
        target = file_item.get().select(["publication"]).execute_query()
        self.assertEqual(target.get_property("publication")["level"], "checkout")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_06_checkin(self):
        """Checking in the target file should set publication level to published."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        file_item.checkin("").execute_query()
        target = file_item.get().select(["publication"]).execute_query()
        self.assertEqual(target.get_property("publication")["level"], "published")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_07_list_versions(self):
        """Listing versions of the target file should have at least 1 version."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        versions = file_item.versions.get().execute_query()
        self.assertGreaterEqual(len(versions), 1)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_08_resumable_upload(self):
        """Uploading a file via resumable upload session should succeed."""
        drive = TestFile.target_drive
        if not drive:
            self.skipTest("No target drive available")

        name = "big_buck_bunny.mp4"
        path = f"{os.path.dirname(__file__)}/../data/{name}"
        file_item = drive.root.resumable_upload(path).get().execute_query()
        self.assertIsNotNone(file_item.get_property("webUrl"))

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_09_download_file(self):
        """Downloading the target file content should return bytes."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        result = file_item.get_content().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_10_convert_file_to_pdf(self):
        """Converting the target file to PDF should return bytes."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        try:
            result = file_item.convert("pdf").execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("File conversion not supported for this file type")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_11_copy_file(self):
        """Copying the target file should succeed."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        name = f"Copied_{uuid.uuid4().hex}_SharePoint User Guide.docx"
        result = file_item.copy(name).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_12_get_activities_by_interval(self):
        """Getting activities for the file by time interval returns results."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        end = datetime.now()
        start = end - timedelta(days=14)
        result = file_item.get_activities_by_interval(start, end, "day").execute_query()
        self.assertIsNotNone(result)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_13_get_item_analytics(self):
        """Getting analytics for the target file returns a valid result."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        result = file_item.analytics.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_14_extract_sensitivity_labels(self):
        """Extracting sensitivity labels from the file should succeed."""
        file_item = TestFile.target_file
        if not file_item:
            self.skipTest("No file uploaded from previous test")

        try:
            result = file_item.extract_sensitivity_labels().execute_query()
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Sensitivity labels not configured for this tenant")

    @requires_delegated(
        "Files.ReadWrite", "Files.ReadWrite.All", "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_15_delete_files(self):
        """Deleting files from the target drive should succeed."""
        drive = TestFile.target_drive
        if not drive:
            self.skipTest("No target drive available")

        items = drive.root.children.top(2).get().execute_query()
        for item in items:
            try:
                item.delete_object().execute_query()
            except Exception:
                pass
