from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.lists.currency import CurrencyList
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.templates.type import ListTemplateType
from office365.sharepoint.permissions.base_permissions import BasePermissions

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPList(SPTestCase):
    """SharePoint list operations tests"""

    target_list: ClassVar[Optional[List]] = None
    target_list_title = create_unique_name("Tasks")

    def test_01_create_list(self):
        """Create a SharePoint list"""
        result = self.client.web.lists.add_list(
            title=self.target_list_title,
            allow_content_types=True,
            template_type=ListTemplateType.TasksWithTimelineAndHierarchy,
        ).execute_query()
        self.assertEqual(result.title, self.target_list_title)
        TestSPList.target_list = result

    def test_02_read_list_by_title(self):
        """Read list by title"""
        result = self.client.web.lists.get_by_title(self.target_list_title).get().execute_query()
        self.assertEqual(self.target_list_title, result.title)

    def test_03_read_list_by_id(self):
        """Read list by ID"""
        self.assertIsNotNone(TestSPList.target_list)
        self.assertIsNotNone(TestSPList.target_list.id)
        result = self.client.web.lists.get_by_id(TestSPList.target_list.id).get().execute_query()
        self.assertEqual(TestSPList.target_list.id, result.id)

    def test_04_read_list_fields(self):
        """Read list related fields"""
        self.assertIsNotNone(TestSPList.target_list)
        result = TestSPList.target_list.get_related_fields().get().execute_query()
        self.assertGreater(len(result), 0)

    def test_05_update_list(self):
        """Update list properties"""
        self.assertIsNotNone(TestSPList.target_list)
        list_to_update = TestSPList.target_list
        self.target_list_title += "_updated"
        list_to_update.set_property("Title", self.target_list_title).update().execute_query()

        result = self.client.web.lists.filter(f"Title eq '{self.target_list_title}'").get().execute_query()
        self.assertEqual(len(result), 1)

    def test_06_get_list_permissions(self):
        """Get effective permissions for current user on the list"""
        self.assertIsNotNone(TestSPList.target_list)
        user = self.client.web.current_user
        result = TestSPList.target_list.get_user_effective_permissions(user).execute_query()
        self.assertIsInstance(result.value, BasePermissions)

    def test_07_get_list_changes(self):
        """Get list change log"""
        self.assertIsNotNone(TestSPList.target_list)
        result = TestSPList.target_list.get_changes().execute_query()
        self.assertGreater(len(result), 0)

    # def test_15_get_checked_out_files(self):
    #    result = self.target_list.get_checked_out_files().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    def test_08_delete_list(self):
        """Delete list and verify removal"""
        list_title = self.target_list_title + "_updated"
        self.client.web.lists.get_by_title(list_title).delete_object().execute_query()

        result = self.client.web.lists.filter(f"Title eq '{list_title}'").get().execute_query()
        self.assertEqual(len(result), 0)

    def test_09_get_list_using_path(self):
        """Get list using server-relative path"""
        result = self.client.web.get_list_using_path("SitePages").execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_10_ensure_events_list(self):
        """Ensure events list exists"""
        events_list = self.client.web.lists.ensure_events_list().execute_query()
        self.assertIsNotNone(events_list.resource_path)

    def test_11_get_list_by_server_relative_url(self):
        """Get list by server-relative URL"""
        pages_list = self.client.web.get_list("SitePages").get().execute_query()
        self.assertIsNotNone(pages_list.resource_path)

    def test_12_get_currency_list(self):
        """Get currency list"""
        result = CurrencyList.get_list(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_13_get_list_by_title(self):
        """Get list by display title"""
        site_pages = self.client.web.get_list_by_title("Site Pages").get().execute_query()
        self.assertIsNotNone(site_pages.resource_path)

    def test_14_get_metadata_navigation_settings(self):
        """Get metadata navigation settings for a list"""
        site_pages = self.client.web.get_list_by_title("Site Pages")
        result = site_pages.get_metadata_navigation_settings().execute_query()
        self.assertIsNotNone(result.value)

    def test_15_render_list_data_as_stream(self):
        """Render list data as stream"""
        result = self.client.web.get_list_by_title("Site Pages").render_list_data_as_stream().execute_query()
        self.assertIsInstance(result.value, str)
