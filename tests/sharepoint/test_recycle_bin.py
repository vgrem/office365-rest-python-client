from random import randint

from office365.sharepoint.files.file import File
from office365.sharepoint.recyclebin.item_collection import RecycleBinItemCollection
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointRecycleBin(SPTestCase):
    target_file: File = None

    @classmethod
    def setUpClass(cls):
        super(TestSharePointRecycleBin, cls).setUpClass()
        file_name = "Sample{0}.txt".format(str(randint(0, 10000)))
        target_file = (
            cls.client.web.default_document_library()
            .root_folder.upload_file(file_name, "--some content goes here--")
            .execute_query()
        )
        cls.target_file = target_file

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_recycle_file(self):
        result = self.__class__.target_file.recycle().execute_query()
        self.assertIsNotNone(result.value)

    def test2_find_removed_file(self):
        file_name = self.__class__.target_file.name
        items = (
            self.client.site.recycle_bin.filter("LeafName eq '{0}'".format(file_name))
            .get()
            .execute_query()
        )
        self.assertGreater(len(items), 0)

    def test3_restore_file(self):
        items = self.client.web.recycle_bin.get().execute_query()
        self.assertGreater(len(items), 0)
        items[0].restore().execute_query()
        items_after = self.client.web.recycle_bin.get().execute_query()
        self.assertEqual(len(items_after), len(items) - 1)

    def test4_list_site_recycle_bin_items(self):
        result = self.client.site.get_recycle_bin_items().execute_query()
        self.assertIsInstance(result, RecycleBinItemCollection)
        self.assertIsNotNone(result.resource_path)

    def test5_list_web_recycle_bin_items(self):
        items = self.client.web.get_recycle_bin_items().execute_query()
        self.assertIsInstance(items, RecycleBinItemCollection)

    def test6_clear_recycle_bin(self):
        self.client.site.recycle_bin.delete_all().execute_query()
        items_after = self.client.site.recycle_bin.get().execute_query()
        self.assertEqual(len(items_after), 0)
