"""Tests for SharePoint view operations including creation, fields, rendering, and deletion."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.fields.multi_line_text import FieldMultiLineText
from office365.sharepoint.lists.list import List
from office365.sharepoint.views.create_information import ViewCreationInformation
from office365.sharepoint.views.field_collection import ViewFieldCollection
from office365.sharepoint.views.view import View

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestView(SPTestCase):
    """Test SharePoint view features."""

    target_list: ClassVar[Optional[List]] = None
    target_view: ClassVar[Optional[View]] = None
    target_field: ClassVar[Optional[FieldMultiLineText]] = None
    view_fields_count: ClassVar[Optional[int]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_title = create_unique_name("Tasks")
        field_title = create_unique_name("TaskComment")
        cls.target_list = cls.client.web.lists.add_tasks(list_title).execute_query()
        cls.target_field = cls.target_list.fields.add_note(field_title).execute_query()

    @classmethod
    def tearDownClass(cls):
        target_list = cls.target_list
        if not target_list:
            return
        target_list.delete_object().execute_query()

    def test_01_create_view(self):
        """Create a new view on the target list."""
        target_list = TestView.target_list
        if not target_list:
            self.skipTest("No target list from setup")
        view_properties = ViewCreationInformation()
        view_properties.Title = create_unique_name("My Tasks")
        view_properties.PersonalView = True
        view_properties.Query = """
<View>
  <Query>
    <Where>
      <Eq>
        <FieldRef Name="AssignedTo" />
        <Value Type="Integer">
          <UserID />
        </Value>
      </Eq>
    </Where>
  </Query>
  <ViewFields>
    <FieldRef Name="Title" />
    <FieldRef Name="Status" />
    <FieldRef Name="DueDate" />
    <FieldRef Name="Priority" />
  </ViewFields>
  <RowLimit>100</RowLimit>
</View>
        """

        new_view = target_list.views.add(view_properties).execute_query()
        self.assertEqual(view_properties.Title, new_view.properties["Title"])
        TestView.target_view = new_view

    def test_02_list_views(self):
        """List all views from the target list."""
        target_list = TestView.target_list
        if not target_list:
            self.skipTest("No target list from setup")
        result = target_list.views.get().execute_query()
        self.assertGreater(len(result), 1)

    def test_03_get_view(self):
        """Get the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        result = target_view.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_04_render_as_html(self):
        """Render the target view as HTML."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        result = target_view.render_as_html().execute_query()
        self.assertIsNotNone(result.value)

    def test_05_get_default_view_items(self):
        """Get items from the default view."""
        target_list = TestView.target_list
        if not target_list:
            self.skipTest("No target list from setup")
        result = target_list.default_view.get_items().get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_get_view_items(self):
        """Get items from the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        result = target_view.get_items().get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_07_update_view(self):
        """Update the target view title."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        title_updated = target_view.properties["Title"] + "_updated"
        view_to_update = target_view
        view_to_update.set_property("Title", title_updated).update().execute_query()

        target_list = TestView.target_list
        if not target_list:
            self.skipTest("No target list from setup")
        result = target_list.views.filter(f"Title eq '{title_updated}'").get().execute_query()
        self.assertEqual(len(result), 1)

    def test_08_get_view_fields(self):
        """Get view fields from the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        result = target_view.expand(["ViewFields"]).get().execute_query()
        self.assertIsNotNone(result.view_fields)
        self.assertIsInstance(result.view_fields, ViewFieldCollection)
        TestView.view_fields_count = len(result.view_fields)

    def test_09_add_view_field(self):
        """Add a field to the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        target_field = TestView.target_field
        if not target_field:
            self.skipTest("No target field from setup")
        view_fields_count = TestView.view_fields_count
        if view_fields_count is None:
            self.skipTest("No view fields count from previous test")
        target_view.view_fields.add_view_field(target_field).execute_query()
        after_view_fields = target_view.view_fields.get().execute_query()
        self.assertEqual(view_fields_count + 1, len(after_view_fields))

    def test_10_move_view_field_to(self):
        """Move a view field to a different position."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        target_field = TestView.target_field
        if not target_field:
            self.skipTest("No target field from setup")
        self.assertIsNotNone(target_field.internal_name)
        target_view.view_fields.move_view_field_to(target_field, 2).execute_query()
        result = target_view.view_fields.get().execute_query()
        self.assertEqual(result[2], target_field.internal_name)

    def test_11_remove_view_field(self):
        """Remove a field from the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        target_field = TestView.target_field
        if not target_field:
            self.skipTest("No target field from setup")
        target_view.view_fields.remove_view_field(target_field).execute_query()
        result = target_view.view_fields.get().execute_query()
        view_fields_count = TestView.view_fields_count
        if view_fields_count is None:
            self.skipTest("No view fields count from previous test")
        self.assertEqual(view_fields_count, len(result))

    def test_12_remove_all_view_fields(self):
        """Remove all view fields from the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        target_view.view_fields.remove_all_view_fields().execute_query()
        result = target_view.view_fields.get().execute_query()
        self.assertEqual(0, len(result))

    def test_13_get_view_changes(self):
        """Get change log for view changes."""
        result = self.client.site.get_changes(ChangeQuery(View=True)).execute_query()
        self.assertGreater(len(result), 0)

    def test_14_delete_view(self):
        """Delete the target view."""
        target_view = TestView.target_view
        if not target_view:
            self.skipTest("No target view from previous test")
        view_to_delete = target_view
        view_to_delete.delete_object().execute_query()
