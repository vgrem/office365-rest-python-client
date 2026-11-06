"""Tests for SharePoint taxonomy features including term store, groups, sets, and taxonomy fields."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.fields.field import Field
from office365.sharepoint.lists.list import List
from office365.sharepoint.taxonomy.field import TaxonomyField
from office365.sharepoint.taxonomy.field_value import TaxonomyFieldValue
from office365.sharepoint.taxonomy.field_value_col import TaxonomyFieldValueCollection
from office365.sharepoint.taxonomy.groups.group import TermGroup
from office365.sharepoint.taxonomy.sets.set import TermSet
from office365.sharepoint.taxonomy.stores.store import TermStore
from office365.sharepoint.taxonomy.terms.term import Term

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPTaxonomy(SPTestCase):
    """Test SharePoint taxonomy features."""

    target_field: ClassVar[Optional[Field]] = None
    target_list: ClassVar[Optional[List]] = None
    target_term: ClassVar[Optional[Term]] = None
    target_term_group: ClassVar[Optional[TermGroup]] = None
    target_term_set: ClassVar[Optional[TermSet]] = None

    @classmethod
    def tearDownClass(cls):
        if cls.target_list is not None:
            cls.target_list.delete_object().execute_query()
        super().tearDownClass()

    def test_01_get_term_store(self):
        """Get the term store."""
        term_store = self.client.taxonomy.term_store.get().execute_query()
        self.assertIsInstance(term_store, TermStore)
        self.assertIsNotNone(term_store.name)

    def test_02_get_term_groups(self):
        """Get a term group."""
        term_groups = self.client.taxonomy.term_store.term_groups.get().execute_query()
        self.assertGreater(len(term_groups), 0)
        term_group = term_groups[0]
        self.assertIsInstance(term_group, TermGroup)
        self.assertIsNotNone(term_group.resource_path)
        TestSPTaxonomy.target_term_group = term_group

    def test_03_get_term_sets(self):
        """Get term sets from the target term group."""
        target_term_group = TestSPTaxonomy.target_term_group
        if not target_term_group:
            self.skipTest("No target term group from previous test")
        term_sets = target_term_group.term_sets.get().execute_query()
        self.assertGreater(len(term_sets), 0)
        self.assertIsInstance(term_sets[0], TermSet)
        TestSPTaxonomy.target_term_set = term_sets[0]

    def test_04_get_terms(self):
        """Get terms from the target term set."""
        target_term_set = TestSPTaxonomy.target_term_set
        if not target_term_set:
            self.skipTest("No target term set from previous test")
        terms = target_term_set.terms.get().execute_query()
        self.assertGreater(len(terms), 0)
        self.assertIsInstance(terms[0], Term)
        TestSPTaxonomy.target_term = terms[0]

    def test_05_search_term(self):
        """Search for a term in the term store."""
        result = self.client.taxonomy.term_store.search_term("Sweden").execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_create_list_tax_field(self):
        """Create a taxonomy field on a scratch list."""
        target_term_set = TestSPTaxonomy.target_term_set
        if not target_term_set:
            self.skipTest("No target term set from previous test")
        TestSPTaxonomy.target_list = self.client.web.lists.add_list(create_unique_name("Taxonomy")).execute_query()
        tax_field = TestSPTaxonomy.target_list.fields.create_taxonomy_field(
            name=create_unique_name("Category"), term_set=target_term_set, allow_multiple_values=True
        ).execute_query()
        self.assertIsNotNone(tax_field.resource_path)
        # self.assertTrue(tax_field.properties.get('IsTermSetValid'))
        TestSPTaxonomy.target_field = tax_field

    def test_07_get_tax_field(self):
        """Get and verify the created taxonomy field."""
        target_field = TestSPTaxonomy.target_field
        if not target_field:
            self.skipTest("No target field from previous test")
        existing_field = target_field.get().execute_query()
        self.assertTrue(existing_field.type_as_string, "TaxonomyFieldType")
        self.assertIsInstance(existing_field, TaxonomyField)
        self.assertIsNotNone(existing_field.text_field_id)
        self.assertIsNotNone(existing_field.lookup_list)
        self.assertIsNotNone(existing_field.lookup_web_id)

        text_field = existing_field.text_field.get().execute_query()
        self.assertIsNotNone(text_field.internal_name)

    def test_08_set_tax_value(self):
        """A term is written to the hidden note companion, and the label is its own."""
        target_field = TestSPTaxonomy.target_field
        target_term = TestSPTaxonomy.target_term
        target_list = TestSPTaxonomy.target_list
        if not (target_field and target_term and target_list):
            self.skipTest("No target field from previous test")
        note_name = target_field.text_field.get().execute_query().properties["EntityPropertyName"]
        item = target_list.add_item({"Title": "taxonomy-value"}).execute_query()

        def stored_label():
            items = target_list.get_items().select([note_name]).filter("Title eq 'taxonomy-value'").get()
            note_text = items.execute_query()[0].properties[note_name]
            self.assertTrue(note_text.endswith("|" + target_term.id), note_text)
            return note_text.split("|", 1)[0].split("#", 1)[1]

        def set_term(label):
            values = TaxonomyFieldValueCollection([TaxonomyFieldValue(Label=label, TermGuid=target_term.id)])
            item.set_property(target_field.internal_name, values)
            item.update().execute_query()

        # The term id identifies the value, so an unlabelled term carries an empty
        # label -- not the word "None", which is what the column stored and read
        # back when ``str()`` rendered a missing label literally.
        set_term(None)
        self.assertEqual("", stored_label())

        # A labelled term keeps the label it was given.
        label = target_term.labels[0].name
        set_term(label)
        self.assertEqual(label, stored_label())

    def test_09_delete_tax_field(self):
        """Delete the created taxonomy field."""
        target_field = TestSPTaxonomy.target_field
        if not target_field:
            self.skipTest("No target field from previous test")
        target_field.delete_object().execute_query()
