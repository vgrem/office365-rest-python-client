"""Tests for SharePoint recycle bin operations including recycling, restoring, and clearing items."""

from __future__ import annotations

from random import randint
from typing import ClassVar, Optional

from office365.sharepoint.files.file import File
from office365.sharepoint.recyclebin.item_collection import RecycleBinItemCollection

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointRecycleBin(SPTestCase):
    """Test SharePoint recycle bin features."""

    target_file: ClassVar[Optional[File]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        file_name = f"Sample{str(randint(0, 10000))}.txt"
        target_file = (
            cls.client.web.default_document_library()
            .root_folder.upload_file(file_name, "--some content goes here--")
            .execute_query()
        )
        cls.target_file = target_file

    @classmethod
    def tearDownClass(cls):
        pass

    def test_01_recycle_file(self):
        """Recycle a file and verify the operation result."""
        target = TestSharePointRecycleBin.target_file
        if not target:
            self.skipTest("No target file from previous test")
        result = target.recycle().execute_query()
        self.assertIsNotNone(result.value)

    def test_02_find_removed_file(self):
        """Find a recycled file in the site recycle bin."""
        target = TestSharePointRecycleBin.target_file
        if not target:
            self.skipTest("No target file from previous test")
        file_name = target.name
        items = self.client.site.recycle_bin.filter(f"LeafName eq '{file_name}'").get().execute_query()
        self.assertGreater(len(items), 0)

    def test_03_restore_file(self):
        """Restore a file from the web recycle bin."""
        items = self.client.web.recycle_bin.get().execute_query()
        self.assertGreater(len(items), 0)
        items[0].restore().execute_query()
        items_after = self.client.web.recycle_bin.get().execute_query()
        self.assertEqual(len(items_after), len(items) - 1)

    def test_04_list_site_recycle_bin_items(self):
        """List site-level recycle bin items."""
        result = self.client.site.get_recycle_bin_items().execute_query()
        self.assertIsInstance(result, RecycleBinItemCollection)
        self.assertIsNotNone(result.resource_path)

    def test_05_list_web_recycle_bin_items(self):
        """List web-level recycle bin items."""
        items = self.client.web.get_recycle_bin_items().execute_query()
        self.assertIsInstance(items, RecycleBinItemCollection)

    def test_06_clear_recycle_bin(self):
        """Clear all items from the site recycle bin."""
        self.client.site.recycle_bin.delete_all().execute_query()
        items_after = self.client.site.recycle_bin.get().execute_query()
        self.assertEqual(len(items_after), 0)
