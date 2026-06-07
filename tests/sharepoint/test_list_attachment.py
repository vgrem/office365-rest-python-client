from __future__ import annotations

import os.path
from io import BytesIO
from typing import ClassVar, Optional

from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.listitems.listitem import ListItem

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestListItemAttachment(SPTestCase):
    """List item attachment operations tests"""

    attachment_file_name = "Sample.txt"
    target_item: ClassVar[Optional[ListItem]] = None
    attachment_path = f"{os.path.dirname(__file__)}/../data/{attachment_file_name}"
    target_attachment: ClassVar[Optional[Attachment]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_name = create_unique_name("Tasks")
        target_list = cls.client.web.lists.add_tasks(list_name).execute_query()
        item_properties = {"Title": "Approval Task"}
        cls.target_item = target_list.add_item(item_properties).execute_query()

    @classmethod
    def tearDownClass(cls):
        assert cls.target_item is not None
        cls.target_item.delete_object().execute_query()
        cls.target_item.parent_list.delete_object().execute_query()

    def test_01_upload_attachment(self):
        """Upload an attachment to a list item"""
        self.assertIsNotNone(TestListItemAttachment.target_item)
        with open(self.attachment_path, "rb") as f:
            result = TestListItemAttachment.target_item.attachment_files.upload(f).execute_query()
        self.assertIsNotNone(result.file_name)
        TestListItemAttachment.target_attachment = result

    def test_02_list_attachments(self):
        """List all attachments on a list item"""
        self.assertIsNotNone(TestListItemAttachment.target_item)
        result = TestListItemAttachment.target_item.attachment_files.get().execute_query()
        self.assertEqual(len(result), 1)

    def test_03_get_by_filename(self):
        """Get attachment by filename"""
        self.assertIsNotNone(TestListItemAttachment.target_item)
        result = TestListItemAttachment.target_item.attachment_files.get_by_filename(self.attachment_file_name)
        self.assertIsNotNone(result.resource_path)

    def test_04_download_attachment(self):
        """Download attachment content"""
        self.assertIsNotNone(TestListItemAttachment.target_attachment)
        f = BytesIO()
        TestListItemAttachment.target_attachment.download(f).execute_query()
        self.assertIsNotNone(f.read())

    def test_05_update_attachment(self):
        """Update attachment content"""
        self.assertIsNotNone(TestListItemAttachment.target_attachment)
        local_f = BytesIO(b"new attachment content goes here")
        TestListItemAttachment.target_attachment.upload(local_f).execute_query()

        remote_f = BytesIO()
        TestListItemAttachment.target_attachment.download(remote_f).execute_query()
        local_content = local_f.getvalue()
        remote_content = remote_f.getvalue()
        self.assertEqual(local_content, remote_content)

    def test_06_delete_attachments(self):
        """Delete attachment and verify"""
        self.assertIsNotNone(TestListItemAttachment.target_attachment)
        self.assertIsNotNone(TestListItemAttachment.target_item)
        TestListItemAttachment.target_attachment.delete_object().execute_query()
        result = TestListItemAttachment.target_item.attachment_files.get().execute_query()
        self.assertEqual(len(result), 0)
