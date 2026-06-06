"""Tests for SharePoint taxonomy features including term store, groups, sets, and taxonomy fields."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.fields.field import Field
from office365.sharepoint.taxonomy.field import TaxonomyField
from office365.sharepoint.taxonomy.groups.group import TermGroup
from office365.sharepoint.taxonomy.sets.set import TermSet
from office365.sharepoint.taxonomy.stores.store import TermStore
from office365.sharepoint.taxonomy.terms.term import Term

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPTaxonomy(SPTestCase):
    """Test SharePoint taxonomy features."""

    target_field: ClassVar[Optional[Field]] = None
    target_term_group: ClassVar[Optional[TermGroup]] = None
    target_term_set: ClassVar[Optional[TermSet]] = None

    def test_01_get_term_store(self):
        """Get the term store."""
        term_store = self.client.taxonomy.term_store.get().execute_query()
        self.assertIsInstance(term_store, TermStore)
        self.assertIsNotNone(term_store.name)

    def test_02_get_term_groups(self):
        """Get a term group by name."""
        term_group = self.client.taxonomy.term_store.term_groups.get_by_name("Geography").get().execute_query()
        self.assertIsNotNone(term_group.resource_path)
        self.assertIsInstance(term_group, TermGroup)
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

    def test_05_search_term(self):
        """Search for a term in the term store."""
        result = self.client.taxonomy.term_store.search_term("Sweden").execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_create_list_tax_field(self):
        """Create a taxonomy field on the default document library."""
        term_set_id = "b49f64b3-4722-4336-9a5c-56c326b344d4"
        tax_field = (
            self.client.web.default_document_library()
            .fields.create_taxonomy_field(name="Category123", term_set=term_set_id)
            .execute_query()
        )
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

    def test_08_delete_tax_field(self):
        """Delete the created taxonomy field."""
        target_field = TestSPTaxonomy.target_field
        if not target_field:
            self.skipTest("No target field from previous test")
        target_field.delete_object().execute_query()
