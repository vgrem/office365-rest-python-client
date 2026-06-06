"""Tests for SharePoint field operations (CRUD on site fields)."""

from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from office365.sharepoint.fields.field import Field
from office365.sharepoint.fields.text import FieldText

from tests.sharepoint.sharepoint_case import SPTestCase


class TestField(SPTestCase):
    """Tests for SharePoint field lifecycle operations."""

    target_field: ClassVar[Optional[Field]] = None
    target_field_name = "Title"

    def test_01_get_site_fields(self):
        """Get top-level site fields."""
        result = self.client.site.root_web.fields.top(10).get().execute_query()
        self.assertGreater(len(result), 0)

    def test_02_get_field(self):
        """Get a field by internal name and verify its type."""
        field = (
            self.client.site.root_web.fields.get_by_internal_name_or_title(self.target_field_name).get().execute_query()
        )
        self.assertIsNotNone(field.internal_name)
        self.assertEqual(field.internal_name, self.target_field_name)
        self.assertIsInstance(field, FieldText)
        self.assertIsNotNone(field.max_length)

    def test_03_get_field_by_title(self):
        """Get a field by its display title."""
        title_field = self.client.site.root_web.fields.get_by_title(self.target_field_name).get().execute_query()
        self.assertIsNotNone(title_field.internal_name)
        self.assertEqual(title_field.internal_name, self.target_field_name)

    def test_04_create_site_field(self):
        """Create a new text field on the site."""
        field_name = "Title_" + uuid.uuid4().hex
        field = self.client.site.root_web.fields.add_text_field(field_name).execute_query()
        self.assertEqual(field.title, field_name)
        self.assertIsInstance(field, FieldText)
        TestField.target_field = field

    def test_05_update_site_field(self):
        """Update the title of a site field."""
        target = TestField.target_field
        if not target:
            self.skipTest("No resource from previous test")
        field = target
        updated_field_name = "Title_" + uuid.uuid4().hex
        field.set_property("Title", updated_field_name).update().execute_query()

        updated_field = self.client.site.root_web.fields.get_by_title(updated_field_name).get().execute_query()
        self.assertIsNotNone(updated_field.id)
        self.assertEqual(updated_field.title, updated_field_name)

    def test_06_delete_site_field(self):
        """Delete a site field."""
        target = TestField.target_field
        if not target:
            self.skipTest("No resource from previous test")
        target.delete_object().execute_query()
