from __future__ import annotations

import os.path
from io import BytesIO

from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.listitems.listitem import ListItem

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestListItemAttachment(SPTestCase):
    attachment_file_name = "Sample.txt"
    target_item: ListItem | None = None
    attachment_path = f"{os.path.dirname(__file__)}/../data/{attachment_file_name}"
    target_attachment: Attachment | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_name = create_unique_name("Tasks")
        target_list = cls.client.web.lists.add_tasks(list_name).execute_query()
        item_properties = {"Title": "Approval Task"}
        cls.target_item = target_list.add_item(item_properties).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_item.delete_object().execute_query()
        cls.target_item.parent_list.delete_object().execute_query()

    def test1_upload_attachment(self):
        with open(self.attachment_path, "rb") as f:
            result = self.target_item.attachment_files.upload(f).execute_query()
        self.assertIsNotNone(result.file_name)
        type(self).target_attachment = result

    def test2_list_attachments(self):
        result = self.target_item.attachment_files.get().execute_query()
        self.assertEqual(len(result), 1)

    def test3_get_by_filename(self):
        result = self.target_item.attachment_files.get_by_filename(self.attachment_file_name)
        self.assertIsNotNone(result.resource_path)

    def test4_download_attachment(self):
        assert self.target_attachment is not None
        f = BytesIO()
        self.target_attachment.download(f).execute_query()
        self.assertIsNotNone(f.read())

    def test5_update_attachment(self):
        assert self.target_attachment is not None
        local_f = BytesIO(b"new attachment content goes here")
        self.target_attachment.upload(local_f).execute_query()

        remote_f = BytesIO()
        self.target_attachment.download(remote_f).execute_query()
        local_content = local_f.getvalue()
        remote_content = remote_f.getvalue()
        self.assertEqual(local_content, remote_content)

    def test6_delete_attachments(self):
        assert self.target_attachment is not None
        self.target_attachment.delete_object().execute_query()
        result = self.target_item.attachment_files.get().execute_query()
        self.assertEqual(len(result), 0)
