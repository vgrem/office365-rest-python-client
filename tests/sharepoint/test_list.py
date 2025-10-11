from office365.sharepoint.lists.creation_information import ListCreationInformation
from office365.sharepoint.lists.currency import CurrencyList
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.template_type import ListTemplateType
from office365.sharepoint.permissions.base_permissions import BasePermissions
from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPList(SPTestCase):
    target_list: List = None
    target_list_title = create_unique_name("Tasks")

    def test_10_create_list(self):
        list_properties = ListCreationInformation()
        list_properties.AllowContentTypes = True
        list_properties.BaseTemplate = ListTemplateType.TasksWithTimelineAndHierarchy
        list_properties.Title = self.target_list_title
        list_to_create = self.client.web.lists.add(list_properties).execute_query()
        self.assertEqual(list_properties.Title, list_to_create.title)
        self.__class__.target_list = list_to_create

    def test_11_read_list_by_title(self):
        result = self.client.web.lists.get_by_title(self.target_list_title).get().execute_query()
        self.assertEqual(self.target_list_title, result.title)

    def test_12_read_list_by_id(self):
        result = self.client.web.lists.get_by_id(self.__class__.target_list.id).get().execute_query()
        self.assertEqual(self.target_list.id, result.id)

    def test_13_read_list_fields(self):
        result = self.__class__.target_list.get_related_fields().get().execute_query()
        self.assertGreater(len(result), 0)

    def test_14_update_list(self):
        list_to_update = self.__class__.target_list
        self.target_list_title += "_updated"
        list_to_update.set_property("Title", self.target_list_title).update().execute_query()

        result = self.client.web.lists.filter(f"Title eq '{self.target_list_title}'").get().execute_query()
        self.assertEqual(len(result), 1)

    def test_15_get_list_permissions(self):
        user = self.client.web.current_user
        result = self.__class__.target_list.get_user_effective_permissions(user).execute_query()
        self.assertIsInstance(result.value, BasePermissions)

    def test_16_get_list_changes(self):
        result = self.__class__.target_list.get_changes().execute_query()
        self.assertGreater(len(result), 0)

    # def test_15_get_checked_out_files(self):
    #    result = self.__class__.target_list.get_checked_out_files().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    def test_17_delete_list(self):
        list_title = self.target_list_title + "_updated"
        self.client.web.lists.get_by_title(list_title).delete_object().execute_query()

        result = self.client.web.lists.filter(f"Title eq '{list_title}'").get().execute_query()
        self.assertEqual(len(result), 0)

    def test_18_get_list_using_path(self):
        result = self.client.web.get_list_using_path("SitePages").execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_19_ensure_events_list(self):
        events_list = self.client.web.lists.ensure_events_list().execute_query()
        self.assertIsNotNone(events_list.resource_path)

    def test_20_get_list_by_server_relative_url(self):
        pages_list = self.client.web.get_list("SitePages").get().execute_query()
        self.assertIsNotNone(pages_list.resource_path)

    def test_21_get_currency_list(self):
        result = CurrencyList.get_list(self.client).execute_query()
        self.assertIsNotNone(result.value)

    def test_23_get_list_by_title(self):
        site_pages = self.client.web.get_list_by_title("Site Pages").get().execute_query()
        self.assertIsNotNone(site_pages.resource_path)

    def test_24_get_metadata_navigation_settings(self):
        site_pages = self.client.web.get_list_by_title("Site Pages")
        result = site_pages.get_metadata_navigation_settings().execute_query()
        self.assertIsNotNone(result.value)

    def test_25_render_list_data_as_stream(self):
        result = self.client.web.get_list_by_title("Site Pages").render_list_data_as_stream().execute_query()
        self.assertIsInstance(result.value, str)
