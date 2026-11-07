"""A column's ``SchemaXml`` is copied, repointed and read back as XML.

Live, because the payload is only proven by the service taking it: the assertions
below are about what SharePoint accepted (a new lookup column that resolves against
the list it was repointed at) rather than about a string this code produced.
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.migration.sharepoint.structure import comparable_schema, rewrite_lookup_schema
from office365.runtime.converters.scalars import normalize_guid
from office365.sharepoint.fields.field import Field
from office365.sharepoint.fields.schema import ORIGIN_ATTRIBUTES, FieldSchema
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.templates.type import ListTemplateType

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase

_FIELD_SELECT = ["Id", "InternalName", "TypeAsString", "SchemaXml", "AllowMultipleValues"]


class TestFieldSchema(SPTestCase):
    """Schema edits against a real column, on scratch lists this class removes."""

    source_list: ClassVar[List]
    target_list: ClassVar[List]
    lookup: ClassVar[Field]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.source_list = cls.client.web.lists.add_list(
            create_unique_name("SchemaSource"), template_type=ListTemplateType.GenericList
        ).execute_query()
        cls.target_list = cls.client.web.lists.add_list(
            create_unique_name("SchemaTarget"), template_type=ListTemplateType.GenericList
        ).execute_query()
        # A lookup names the list it resolves against in its schema, which is the
        # attribute a replay has to repoint -- and the only way to get one is to ask
        # the service for it.
        cls.lookup = cls.source_list.fields.add_lookup_field(
            title="RelatedItem", lookup_list=cls.target_list, lookup_field_name="Title"
        ).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.source_list.delete_object().execute_query()
        cls.target_list.delete_object().execute_query()

    def _read(self, sp_list: List, internal_name: str) -> Field:
        fields = sp_list.fields.select(_FIELD_SELECT).get().execute_query()
        read: Optional[Field] = next((field for field in fields if field.internal_name == internal_name), None)
        if read is None:  # pragma: no cover - a missing column is the failure itself
            self.fail(f"column '{internal_name}' is missing from {sp_list.title!r}")
        return read

    def test_01_a_copied_schema_names_no_origin(self):
        """The pair the service rejects on another site is gone; nothing else moved."""
        field = self._read(self.source_list, self.lookup.internal_name)
        # The service writes both attributes on a column created from a schema.
        self.assertIn("SourceID", field.schema_xml or "")
        self.assertIn("Version", field.schema_xml or "")

        copied = field.schema_xml_for_copy()
        self.assertIsNotNone(copied)
        for name in ORIGIN_ATTRIBUTES:
            self.assertNotIn(name, copied)
        # The live read is the edit, not a second spelling of it.
        self.assertEqual(copied, FieldSchema.parse(field.schema_xml).without_origin_attributes().to_xml())

    def test_02_a_rewritten_lookup_resolves_against_the_list_it_names(self):
        """Rewritten to the other list and created there, the column reads back repointed."""
        field = self._read(self.source_list, self.lookup.internal_name)
        rewritten, unresolved = rewrite_lookup_schema(
            field.schema_xml_for_copy(),
            {normalize_guid(self.target_list.id): normalize_guid(self.source_list.id)},
        )
        self.assertIsNone(unresolved)
        self.assertIsNotNone(rewritten)
        self.assertEqual(FieldSchema.parse(rewritten).list_id, "{%s}" % normalize_guid(self.source_list.id))

        self.target_list.fields.ensure_xml(rewritten, "RelatedItem", on_conflict="update").execute_query()

        read_back = self._read(self.target_list, "RelatedItem")
        self.assertEqual(read_back.type_as_string, "Lookup")
        self.assertEqual(FieldSchema.parse(read_back.schema_xml).list_id, FieldSchema.parse(rewritten).list_id)
        # The service echoed the definition back; only the origin attributes it adds
        # itself (and the list id, which is by definition different) are ignored.
        self.assertEqual(comparable_schema(rewritten), comparable_schema(read_back.schema_xml))

    def test_03_an_edit_reaches_the_root_and_nothing_else(self):
        """A child that carries the same attribute names is left alone.

        ``FieldRefs`` children do carry them on a real tenant (304 ``<FieldRef
        List=...>`` across 7,751 schemas), which is why the edit reads the root
        rather than searching the document.
        """
        field = self._read(self.source_list, self.lookup.internal_name)
        self.assertIsNotNone(FieldSchema.parse(field.schema_xml))

        child = '<FieldRef Name="Title" SourceID="{%s}" Version="4" />' % (normalize_guid(self.target_list.id) or "")
        # The service hands back one self-closing element; give it the one child this
        # assertion is about. The string never reaches the service.
        opening = field.schema_xml.strip()
        self.assertTrue(opening.endswith("/>"))
        with_child = opening[: -len("/>")].rstrip() + ">" + child + "</Field>"

        copied = FieldSchema.parse(with_child).without_origin_attributes().to_xml()
        self.assertIn(child, copied)

        repointed = FieldSchema.parse(with_child).with_list(normalize_guid(self.source_list.id) or "").to_xml()
        self.assertIn(child, repointed)
        self.assertEqual(FieldSchema.parse(repointed).list_id, "{%s}" % normalize_guid(self.source_list.id))
