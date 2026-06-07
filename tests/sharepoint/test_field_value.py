"""Tests for SharePoint field value operations (text, multi-choice, user, lookup, URL, geo, choice)."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.fields.choice import FieldChoice
from office365.sharepoint.fields.multi_choice import FieldMultiChoice
from office365.sharepoint.fields.multi_lookup_value import FieldMultiLookupValue
from office365.sharepoint.fields.multi_user_value import FieldMultiUserValue
from office365.sharepoint.fields.user_value import FieldUserValue
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestFieldValue(SPTestCase):
    """Tests for SharePoint list item field values of various types."""

    target_item: ClassVar[Optional[ListItem]] = None
    target_field: ClassVar[Optional[FieldMultiChoice]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.multi_lookup_field_name = "PredecessorsAlt2"
        cls.url_field_name = "DocumentationLink"
        cls.geo_field_name = "Place"
        cls.choice_field_name = "TaskStatus"
        cls.multi_choice_field_name = "TaskStatuses"
        cls.user_field_name = "PrimaryApprover"
        cls.user_multi_field_name = "SecondaryApprovers"
        cls.lookup_field_name = "RelatedDocuments"
        list_title: str = create_unique_name("Tasks N")
        cls.target_list: List = cls.client.web.lists.add_tasks(list_title).execute_query()
        cls.lookup_list = cls.client.web.default_document_library().get().execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_list.delete_object().execute_query()

    def test_01_get_web_available_fields(self):
        """Get available fields for the web."""
        result = self.client.web.available_fields.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_02_set_field_text_value(self):
        """Set a text field value on a new list item."""
        items = self.target_list.items
        create_info = {
            "Title": "Task1",
        }
        TestFieldValue.target_item = self.target_list.add_item(create_info).execute_query()
        self.client.load(items)
        self.client.execute_query()
        self.assertGreaterEqual(len(items), 1)

    def test_03_create_multi_lookup_field(self):
        """Create a multi-lookup field on the target list."""
        result = self.target_list.fields.add_lookup_field(
            title=self.multi_lookup_field_name,
            lookup_list=self.target_list,
            lookup_field_name="Title",
            allow_multiple_values=True,
        ).execute_query()
        self.assertEqual(result.type_as_string, "LookupMulti")

    def test_04_set_field_multi_lookup_value(self):
        """Set a multi-lookup field value on the target item."""
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        self.assertIsNotNone(target.id)
        updated = target.set_multi_lookup_field_value(self.multi_lookup_field_name, [target.id]).execute_query()
        self.assertIsInstance(updated.properties[self.multi_lookup_field_name], FieldMultiLookupValue)

    def test_05_create_user_multi_field(self):
        """Create a multi-user field on the target list."""
        geo_field = self.target_list.fields.add_user_field(
            self.user_multi_field_name, allow_multiple_values=True
        ).execute_query()
        self.assertIsNotNone(geo_field.resource_path)
        self.assertEqual(geo_field.type_as_string, "UserMulti")

    def test_06_set_field_multi_user_value(self):
        """Set a multi-user field value on the target item."""
        current_user = self.client.web.current_user
        value = FieldMultiUserValue()
        value.add(FieldUserValue.from_user(current_user))
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_property(self.user_multi_field_name, value).update().execute_query()
        self.assertIsNotNone(target.properties.get(self.user_multi_field_name))

    def test_07_create_list_multi_choice_field(self):
        """Create a multi-choice field on the target list."""
        choices = ["Not Started", "In Progress", "Completed", "Deferred"]
        result = self.target_list.fields.add_choice_field(
            title=self.multi_choice_field_name, values=choices, multiple_values=True
        ).execute_query()
        self.assertIsInstance(result, FieldMultiChoice)
        TestFieldValue.target_field = result

    def test_08_set_field_multi_choice_value(self):
        """Set a multi-choice field value on the target item."""
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_choice_field_value(self.multi_choice_field_name, ["In Progress"]).execute_query()
        self.assertIsNotNone(target.properties.get(self.multi_choice_field_name))

    def test_09_create_list_choice_field(self):
        """Create a choice field on the target list."""
        choices = ["Not Started", "In Progress", "Completed", "Deferred"]
        created_field = self.target_list.fields.add_choice_field(
            title=self.choice_field_name, values=choices
        ).execute_query()
        self.assertIsInstance(created_field, FieldChoice)

    def test_10_set_field_choice_value(self):
        """Set a choice field value on the target item."""
        choice_value = "In Progress"
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_choice_field_value(self.choice_field_name, choice_value).execute_query()
        self.assertIsNotNone(target.properties.get(self.choice_field_name))

    def test_11_get_lookup_field_choices(self):
        """Get lookup field choices from the target list."""
        result = self.target_list.get_lookup_field_choices(self.multi_choice_field_name).execute_query()
        self.assertIsNotNone(result.value)

    def test_12_create_list_url_field(self):
        """Create a URL field on the target list."""
        result = self.target_list.fields.add_url_field(self.url_field_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.type_as_string, "URL")

    def test_13_set_url_field_value(self):
        """Set a URL field value on the target item."""
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_url_field_value(
            self.url_field_name,
            "https://docs.microsoft.com/en-us/previous-versions/office/sharepoint-server/ms472498(v=office.15)",
        ).execute_query()
        self.assertIsNotNone(target.properties.get(self.url_field_name))

    def test_14_create_list_geolocation_field(self):
        """Create a geolocation field on the target list."""
        geo_field = self.target_list.fields.add_geolocation_field(self.geo_field_name).execute_query()
        self.assertIsNotNone(geo_field.resource_path)
        self.assertEqual(geo_field.type_as_string, "Geolocation")

    def test_15_set_geo_field_value(self):
        """Set a geolocation field value on the target item."""
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_geo_field_value(self.geo_field_name, 59.940117, 29.8145056).execute_query()
        self.assertIsNotNone(target.properties.get(self.geo_field_name))

    def test_16_create_list_user_field(self):
        """Create a user field on the target list."""
        user_field = self.target_list.fields.add_user_field(self.user_field_name).execute_query()
        self.assertIsNotNone(user_field.resource_path)
        self.assertEqual(user_field.type_as_string, "User")

    def test_17_set_user_field_value(self):
        """Set a user field value on the target item."""
        current_user = self.client.web.current_user
        user_value = FieldUserValue.from_user(current_user)
        target = TestFieldValue.target_item
        if not target:
            self.skipTest("No resource from previous test")
        target.set_property(self.user_field_name, user_value).update().execute_query()
        self.assertIsNotNone(target.properties.get(self.user_field_name))

    def test_18_create_list_lookup_field(self):
        """Create a lookup field on the target list."""
        lookup_field = self.target_list.fields.add_lookup_field(
            title=self.lookup_field_name,
            lookup_list=self.lookup_list.properties["Id"],
            lookup_field_name="Title",
        ).execute_query()
        self.assertEqual(lookup_field.type_as_string, "Lookup")

    def test_19_set_lookup_field_value(self):
        """Set a lookup field value on the target item."""
        lookup_items = self.client.web.default_document_library().get_items().execute_query()
        if len(lookup_items) > 0:
            target = TestFieldValue.target_item
            if not target:
                self.skipTest("No resource from previous test")
            target.set_lookup_field_value(self.lookup_field_name, lookup_items[0].properties["Id"]).execute_query()
            self.assertIsNotNone(target.properties.get(self.lookup_field_name))
