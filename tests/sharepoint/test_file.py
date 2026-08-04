from __future__ import annotations

import os
from io import BytesIO
from typing import ClassVar, Optional

from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.files.file import File
from office365.sharepoint.folders.folder import Folder

from tests import create_unique_name, test_cert_path, test_cert_thumbprint, test_client_id, test_tenant
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointFile(SPTestCase):
    """SharePoint file operations tests"""

    folder_from: ClassVar[Optional[Folder]] = None
    folder_to: ClassVar[Optional[Folder]] = None
    file: ClassVar[Optional[File]] = None
    deleted_file_guid: ClassVar[Optional[str]] = None
    text_content = b"updated content goes here..."

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.folder_from = cls.client.web.default_document_library().root_folder.add(create_unique_name("from"))
        cls.folder_to = cls.client.web.default_document_library().root_folder.add(create_unique_name("to"))
        assert cls.folder_from.resource_path is not None
        assert cls.folder_to.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        assert cls.folder_from is not None
        assert cls.folder_to is not None
        cls.folder_from.delete_object().execute_query()
        cls.folder_to.delete_object().execute_query()

    def test_01_upload_file_as_content(self):
        """Upload a file as binary content"""
        folder = TestSharePointFile.folder_from
        assert folder is not None
        path = f"{os.path.dirname(__file__)}/../data/Sample.txt"
        uploaded_file = folder.files.upload(path).execute_query()
        self.assertEqual(uploaded_file.name, os.path.basename(path))
        self.assertIsNotNone(uploaded_file.resource_path)
        TestSharePointFile.file = uploaded_file

    def test_02_get_first_file(self):
        """Get first file from folder"""
        folder = TestSharePointFile.folder_from
        assert folder is not None
        files = folder.files.top(1).get().execute_query()
        self.assertEqual(len(files), 1)

    def test_03_get_file_from_absolute_url(self):
        """Get file from absolute URL"""
        file = TestSharePointFile.file
        assert file is not None
        result = file.get_absolute_url().execute_query()
        self.assertIsNotNone(result.value)
        file = (
            File.from_url(result.value)
            .with_client_certificate(
                test_tenant,
                client_id=test_client_id,
                thumbprint=test_cert_thumbprint,
                cert_path=test_cert_path,
            )
            .get()
            .execute_query()
        )
        self.assertIsNotNone(file.server_relative_url)

    def test_04_create_file_anon_link(self):
        """Create anonymous link for file"""
        file = TestSharePointFile.file
        assert file is not None
        result = file.create_anonymous_link(False).execute_query()
        self.assertIsNotNone(result.value)

    def test_05_load_file_metadata(self):
        """Load file metadata"""
        file = TestSharePointFile.file
        assert file is not None
        result = file.listItemAllFields.expand(["File"]).get().execute_query()
        self.assertIsInstance(result.file, File)

    def test_06_load_file_metadata_alt(self):
        """Load file metadata via client"""
        file = TestSharePointFile.file
        assert file is not None
        list_item = file.listItemAllFields
        self.client.load(list_item, ["File"])
        self.client.execute_query()
        self.assertIsInstance(list_item.file, File)

    def test_07_update_file_content(self):
        """Update file binary content"""
        file = TestSharePointFile.file
        assert file is not None
        file = file.save_binary_stream(self.text_content).execute_query()
        self.assertTrue(file.resource_path)

    def test_08_update_file_metadata(self):
        """Update file metadata properties"""
        file = TestSharePointFile.file
        assert file is not None
        list_item = file.listItemAllFields  # get metadata
        list_item.set_property("Title", "Updated")
        list_item.update().execute_query()

    def test_09_list_file_versions(self):
        """List file versions"""
        file = TestSharePointFile.file
        assert file is not None
        file = file.expand(["Versions"]).get().execute_query()
        self.assertGreater(len(file.versions), 0)

    def test_10_delete_file_version(self):
        """Delete a file version"""
        file = TestSharePointFile.file
        assert file is not None
        versions = file.versions.top(1).get().execute_query()
        self.assertEqual(len(versions), 1)
        first_version = versions[0]
        self.assertIsNotNone(first_version.resource_path)
        first_version.delete_object().execute_query()

    def test_11_download_file_content(self):
        """Download file content"""
        file = TestSharePointFile.file
        assert file is not None
        result = file.get_content().execute_query()
        self.assertEqual(result.value, self.text_content)

    def test_12_download_file_content_alt(self):
        """Download file content using BytesIO"""
        file = TestSharePointFile.file
        assert file is not None
        with BytesIO() as f:
            file.download(f).execute_query()
            content = f.getvalue()
        self.assertEqual(content, self.text_content)

    def test_13_copy_file(self):
        """Copy file to another folder"""
        file = TestSharePointFile.file
        folder = TestSharePointFile.folder_to
        assert file is not None
        assert folder is not None
        copied_file = file.copyto(folder, True).execute_query()
        self.assertIsNotNone(copied_file.server_relative_url)

    def test_14_move_file(self):
        """Move file to another folder"""
        file = TestSharePointFile.file
        folder = TestSharePointFile.folder_to
        assert file is not None
        assert folder is not None
        moved_file = file.moveto(folder, 1).get().execute_query()
        self.assertIsNotNone(moved_file.server_relative_url)

    def test_15_recycle_file(self):
        """Recycle file"""
        file = TestSharePointFile.file
        folder = TestSharePointFile.folder_to
        assert file is not None
        assert folder is not None
        files_before = folder.files.get().execute_query()
        result = file.recycle().execute_query()
        self.assertIsNotNone(result.value)
        files_after = folder.files.get().execute_query()
        self.assertEqual(len(files_before) - 1, len(files_after))
        TestSharePointFile.deleted_file_guid = result.value

    def test_16_restore_file(self):
        """Restore recycled file"""
        deleted_file_guid = TestSharePointFile.deleted_file_guid
        assert deleted_file_guid is not None
        result = self.client.web.recycle_bin.get_by_id(deleted_file_guid)
        result.restore().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test_18_create_template_file(self):
    #    file_url = "WikiPage.aspx"
    #    file = self.parent_folder.files.add_template_file(file_url, TemplateFileType.WikiPage).execute_query()
    #    self.assertEqual(file.name, file_url)

    def test_17_get_files_changes(self):
        """Get file change log"""
        file = TestSharePointFile.file
        assert file is not None
        changes = file.listItemAllFields.get_changes(ChangeQuery(Item=True)).execute_query()
        self.assertGreater(len(changes), 0)

    def test_18_delete_file(self):
        """Delete file"""
        file = TestSharePointFile.file
        folder = TestSharePointFile.folder_to
        assert file is not None
        assert folder is not None
        files_before = folder.files.get().execute_query()
        self.assertGreater(len(files_before), 0)
        file.delete_object().execute_query()
        files_after = folder.files.get().execute_query()
        self.assertEqual(len(files_after), len(files_before) - 1)

    def test_19_upload_large_file(self):
        """Upload large file via upload session"""
        folder = TestSharePointFile.folder_from
        assert folder is not None
        path = f"{os.path.dirname(__file__)}/../data/big_buck_bunny.mp4"
        file_size = os.path.getsize(path)
        size_1mb = 1000000
        file = folder.files.create_upload_session(path, size_1mb).execute_query()
        self.assertEqual(file_size, file.length)
