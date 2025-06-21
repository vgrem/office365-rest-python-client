import uuid

from office365.sharepoint.fields.field import Field
from office365.sharepoint.fields.text import FieldText
from tests.sharepoint.sharepoint_case import SPTestCase


class TestField(SPTestCase):
    target_field: Field = None
    target_field_name = "Title"

    def test_1_get_site_fields(self):
        result = self.client.site.root_web.fields.top(10).get().execute_query()
        self.assertGreater(len(result), 0)

    def test_2_get_field(self):
        field = (
            self.client.site.root_web.fields.get_by_internal_name_or_title(
                self.target_field_name
            )
            .get()
            .execute_query()
        )
        self.assertIsNotNone(field.internal_name)
        self.assertEqual(field.internal_name, self.target_field_name)
        self.assertIsInstance(field, FieldText)
        self.assertIsNotNone(field.max_length)

    def test_3_get_field_by_title(self):
        title_field = (
            self.client.site.root_web.fields.get_by_title(self.target_field_name)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(title_field.internal_name)
        self.assertEqual(title_field.internal_name, self.target_field_name)

    def test_4_create_site_field(self):
        field_name = "Title_" + uuid.uuid4().hex
        field = self.client.site.root_web.fields.add_text_field(
            field_name
        ).execute_query()
        self.assertEqual(field.title, field_name)
        self.assertIsInstance(field, FieldText)
        self.__class__.target_field = field

    def test_5_update_site_field(self):
        field = self.__class__.target_field
        updated_field_name = "Title_" + uuid.uuid4().hex
        field.set_property("Title", updated_field_name).update().execute_query()

        updated_field = (
            self.client.site.root_web.fields.get_by_title(updated_field_name)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(updated_field.id)
        self.assertEqual(updated_field.title, updated_field_name)

    def test_6_delete_site_field(self):
        field = self.__class__.target_field
        field.delete_object().execute_query()
