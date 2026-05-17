from office365.sharepoint.changes.query import ChangeQuery
from office365.sharepoint.fields.multi_line_text import FieldMultiLineText
from office365.sharepoint.lists.list import List
from office365.sharepoint.views.create_information import ViewCreationInformation
from office365.sharepoint.views.field_collection import ViewFieldCollection
from office365.sharepoint.views.view import View

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestView(SPTestCase):
    target_list: List = None
    target_view: View = None
    target_field: FieldMultiLineText = None
    view_fields_count = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_title = create_unique_name("Tasks")
        field_title = create_unique_name("TaskComment")
        cls.target_list = cls.client.web.lists.add_tasks(list_title).execute_query()
        cls.target_field = cls.target_list.fields.add_note(field_title).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_list.delete_object().execute_query()

    def test1_create_view(self):
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

        new_view = self.target_list.views.add(view_properties).execute_query()
        self.assertEqual(view_properties.Title, new_view.properties["Title"])
        self.__class__.target_view = new_view

    def test2_list_views(self):
        result = self.target_list.views.get().execute_query()
        self.assertGreater(len(result), 1)

    def test3_get_view(self):
        result = self.__class__.target_view.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test4_render_as_html(self):
        result = self.__class__.target_view.render_as_html().execute_query()
        self.assertIsNotNone(result.value)

    def test5_get_default_view_items(self):
        result = self.target_list.default_view.get_items().get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test6_get_view_items(self):
        result = self.__class__.target_view.get_items().get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test7_update_view(self):
        title_updated = self.__class__.target_view.properties["Title"] + "_updated"
        view_to_update = self.__class__.target_view
        view_to_update.set_property("Title", title_updated).update().execute_query()

        result = self.target_list.views.filter(f"Title eq '{title_updated}'").get().execute_query()
        self.assertEqual(len(result), 1)

    def test8_get_view_fields(self):
        result = self.__class__.target_view.expand(["ViewFields"]).get().execute_query()
        self.assertIsNotNone(result.view_fields)
        self.assertIsInstance(result.view_fields, ViewFieldCollection)
        self.__class__.view_fields_count = len(result.view_fields)

    def test9_add_view_field(self):
        self.target_view.view_fields.add_view_field(self.target_field).execute_query()
        after_view_fields = self.target_view.view_fields.get().execute_query()
        self.assertEqual(self.view_fields_count + 1, len(after_view_fields))

    def test_10_move_view_field_to(self):
        self.target_view.view_fields.move_view_field_to(self.target_field, 2).execute_query()
        result = self.__class__.target_view.view_fields.get().execute_query()
        self.assertEqual(result[2], self.target_field.internal_name)

    def test_11_remove_view_field(self):
        self.target_view.view_fields.remove_view_field(self.target_field).execute_query()
        result = self.target_view.view_fields.get().execute_query()
        self.assertEqual(self.view_fields_count, len(result))

    def test_12_remove_all_view_fields(self):
        self.target_view.view_fields.remove_all_view_fields().execute_query()
        result = self.__class__.target_view.view_fields.get().execute_query()
        self.assertEqual(0, len(result))

    def test_13_get_view_changes(self):
        result = self.client.site.get_changes(ChangeQuery(view=True)).execute_query()
        self.assertGreater(len(result), 0)

    def test_14_delete_view(self):
        view_to_delete = self.__class__.target_view
        view_to_delete.delete_object().execute_query()
