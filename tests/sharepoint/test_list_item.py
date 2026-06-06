from __future__ import annotations

from time import sleep
from typing import ClassVar, Optional

from office365.sharepoint.listitems.caml.query import CamlQuery
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List
from office365.sharepoint.types.wopi_action import SPWOPIAction

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointListItem(SPTestCase):
    """SharePoint list item operations tests"""

    target_list: ClassVar[Optional[List]] = None
    target_item: ClassVar[Optional[ListItem]] = None
    deleted_item_guid: ClassVar[Optional[str]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_title = create_unique_name("Tasks")
        cls.target_list = cls.client.web.lists.add_tasks(list_title).execute_query()
        cls.default_title = create_unique_name("Task")
        cls.batch_items_count = 3

    @classmethod
    def tearDownClass(cls):
        cls.assertIsNotNone(cls.target_list)
        cls.target_list.delete_object().execute_query()

    def test_01_create_list_item(self):
        """Create a list item"""
        item_properties = {"Title": self.default_title}
        self.assertIsNotNone(TestSharePointListItem.target_list)
        new_item = TestSharePointListItem.target_list.add_item(item_properties).execute_query()
        self.assertIsNotNone(new_item.properties["Title"])
        TestSharePointListItem.target_item = new_item

    def test_02_enable_folders_in_list(self):
        """Enable folder creation in list"""
        def _init_list():
            self.assertIsNotNone(TestSharePointListItem.target_list)
            if not TestSharePointListItem.target_list.enable_folder_creation:
                TestSharePointListItem.target_list.enable_folder_creation = True
                TestSharePointListItem.target_list.update().execute_query()
            self.assertTrue(TestSharePointListItem.target_list.enable_folder_creation, "Folder creation enabled")

        self.assertIsNotNone(TestSharePointListItem.target_list)
        TestSharePointListItem.target_list.ensure_property("EnableFolderCreation").after_execute(lambda _: _init_list())

    def test_03_create_folder_in_list(self):
        """Create a folder in the list"""
        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.root_folder.add("Archive").execute_query()
        self.assertIsNotNone(result.server_relative_url)

    def test_04_get_list_item(self):
        """Get list item by ID"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        self.assertIsNotNone(TestSharePointListItem.target_item.id)
        item_id = TestSharePointListItem.target_item.id
        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.get_item_by_id(item_id).get().execute_query()
        self.assertIsNotNone(result.id)

    def test_05_get_list_item_via_caml(self):
        """Get list item via CAML query"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        self.assertIsNotNone(TestSharePointListItem.target_item.id)
        item_id = TestSharePointListItem.target_item.id
        caml_query = CamlQuery.parse(
            f"<Where><Eq><FieldRef Name='ID' /><Value Type='Counter'>{item_id}</Value></Eq></Where>"
        )
        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.get_items(caml_query).execute_query()
        self.assertEqual(len(result), 1)

    def test_06_get_wopi_frame_url(self):
        """Get WOPI frame URL for the list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        result = TestSharePointListItem.target_item.get_wopi_frame_url(SPWOPIAction.default).execute_query()
        self.assertIsNotNone(result.value)

    def test_07_update_listItem(self):
        """Update list item properties"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        item_to_update = TestSharePointListItem.target_item.get().execute_query()
        last_updated = item_to_update.properties["Modified"]

        sleep(1)
        new_title = create_unique_name("Task item")
        item_to_update.set_property("Title", new_title).update()
        self.client.load(item_to_update)  # retrieve updated
        self.client.execute_query()
        self.assertNotEqual(item_to_update.properties["Modified"], last_updated)
        self.assertNotEqual(self.default_title, new_title)

    def test_08_systemUpdate_listItem(self):
        """System update list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        item_to_update = TestSharePointListItem.target_item.get().execute_query()
        last_updated = item_to_update.properties["Modified"]

        new_title = create_unique_name("Task item %s")
        item_to_update.set_property("Title", new_title).system_update()
        self.client.load(item_to_update)  # retrieve updated
        self.client.execute_query()
        self.assertEqual(item_to_update.properties["Modified"], last_updated)
        self.assertNotEqual(self.default_title, new_title)

    def test_09_update_overwrite_version(self):
        """Update list item overwriting version"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        item_to_update = TestSharePointListItem.target_item
        item_to_update.update_overwrite_version().execute_query()

    def test_10_get_comments(self):
        """Get comments on list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        comments = TestSharePointListItem.target_item.get_comments().execute_query()
        self.assertIsNotNone(comments.resource_path)

    def test_11_get_versions(self):
        """Get list item versions"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        versions = TestSharePointListItem.target_item.versions.get().execute_query()
        self.assertIsNotNone(versions.resource_path)

    def test_12_get_dlp_policy_tip(self):
        """Get DLP policy tip for list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        result = TestSharePointListItem.target_item.get_dlp_policy_tip.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_13_enable_comments(self):
        """Enable comments on list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        result = TestSharePointListItem.target_item.set_comments_disabled(False).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_14_recycle_item(self):
        """Recycle list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        item_to_recycle = TestSharePointListItem.target_item
        result = item_to_recycle.recycle().execute_query()
        self.assertIsNotNone(result.value)
        TestSharePointListItem.deleted_item_guid = result.value

    def test_15_restore_item(self):
        """Restore recycled list item"""
        self.assertIsNotNone(TestSharePointListItem.deleted_item_guid)
        recycle_item = self.client.web.recycle_bin.get_by_id(TestSharePointListItem.deleted_item_guid)
        recycle_item.restore().execute_query()
        self.assertIsNotNone(recycle_item.resource_path)

    def test_16_set_rating(self):
        """Set rating on list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        result = TestSharePointListItem.target_item.set_rating(1).execute_query()
        self.assertIsNotNone(result.value)

    def test_17_delete_list_item(self):
        """Delete list item"""
        self.assertIsNotNone(TestSharePointListItem.target_item)
        item_id = TestSharePointListItem.target_item.properties["Id"]
        item_to_delete = TestSharePointListItem.target_item
        item_to_delete.delete_object().execute_query()

        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.items.filter(f"Id eq {item_id}").get().execute_query()
        self.assertEqual(0, len(result))

    def test_18_create_multiple_items(self):
        """Create multiple list items in batch"""
        self.assertIsNotNone(TestSharePointListItem.target_list)
        for i in range(self.batch_items_count):
            item_properties = {"Title": f"Task {i}"}
            TestSharePointListItem.target_list.add_item(item_properties)
        self.client.execute_batch()
        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.items.get().execute_query()
        self.assertEqual(len(result), self.batch_items_count)

    def test_19_get_multiple_items_with_params(self):
        """Get multiple items with query parameters"""
        # test case for when .load with set properties_to_retrieve
        # would ignore all other previously set query params (like top(2))

        self.assertIsNotNone(TestSharePointListItem.target_list)
        items = TestSharePointListItem.target_list.items.top(self.batch_items_count)
        self.client.load(items, ["Id", "AttachmentFiles"])
        self.client.execute_query()
        self.assertLessEqual(len(items), self.batch_items_count)

    def test_20_delete_multiple_items(self):
        """Delete multiple list items"""
        self.assertIsNotNone(TestSharePointListItem.target_list)
        result = TestSharePointListItem.target_list.items.get().execute_query()
        self.assertGreater(len(result), 0)
        [item.delete_object() for item in result]
        self.client.execute_batch()
        self.assertIsNotNone(TestSharePointListItem.target_list)
        items_after = TestSharePointListItem.target_list.items.get().execute_query()
        self.assertEqual(len(items_after), 0)

    def test_21_get_all_items(self):
        """Get all items with paging"""
        users_list = self.client.web.site_user_info_list.get().execute_query()
        result = users_list.items.get_all(page_size=1000).execute_query()
        self.assertIsNotNone(users_list.item_count)
        self.assertLessEqual(len(result), users_list.item_count)
