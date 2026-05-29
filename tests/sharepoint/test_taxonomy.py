from __future__ import annotations

from office365.sharepoint.fields.field import Field
from office365.sharepoint.taxonomy.field import TaxonomyField
from office365.sharepoint.taxonomy.groups.group import TermGroup
from office365.sharepoint.taxonomy.sets.set import TermSet
from office365.sharepoint.taxonomy.stores.store import TermStore
from office365.sharepoint.taxonomy.terms.term import Term

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPTaxonomy(SPTestCase):
    target_field: Field | None = None
    target_term_group: TermGroup | None = None
    target_term_set: TermSet | None = None

    def test1_get_term_store(self):
        term_store = self.client.taxonomy.term_store.get().execute_query()
        self.assertIsInstance(term_store, TermStore)
        self.assertIsNotNone(term_store.name)

    def test2_get_term_groups(self):
        term_group = self.client.taxonomy.term_store.term_groups.get_by_name("Geography").get().execute_query()
        self.assertIsNotNone(term_group.resource_path)
        self.assertIsInstance(term_group, TermGroup)
        TestSPTaxonomy.target_term_group = term_group

    def test3_get_term_sets(self):
        assert self.target_term_group is not None
        term_sets = self.target_term_group.term_sets.get().execute_query()
        self.assertGreater(len(term_sets), 0)
        self.assertIsInstance(term_sets[0], TermSet)
        TestSPTaxonomy.target_term_set = term_sets[0]

    def test4_get_terms(self):
        assert self.target_term_set is not None
        terms = self.target_term_set.terms.get().execute_query()
        self.assertGreater(len(terms), 0)
        self.assertIsInstance(terms[0], Term)

    def test5_search_term(self):
        result = self.client.taxonomy.term_store.search_term("Sweden").execute_query()
        self.assertIsNotNone(result.resource_path)

    def test6_create_list_tax_field(self):
        term_set_id = "b49f64b3-4722-4336-9a5c-56c326b344d4"
        tax_field = (
            self.client.web.default_document_library()
            .fields.create_taxonomy_field(name="Category123", term_set=term_set_id)
            .execute_query()
        )
        self.assertIsNotNone(tax_field.resource_path)
        # self.assertTrue(tax_field.properties.get('IsTermSetValid'))
        TestSPTaxonomy.target_field = tax_field

    def test7_get_tax_field(self):
        assert self.target_field is not None
        existing_field = self.target_field.get().execute_query()
        self.assertTrue(existing_field.type_as_string, "TaxonomyFieldType")
        assert isinstance(existing_field, TaxonomyField)
        self.assertIsNotNone(existing_field.text_field_id)
        self.assertIsNotNone(existing_field.lookup_list)
        self.assertIsNotNone(existing_field.lookup_web_id)

        text_field = existing_field.text_field.get().execute_query()
        self.assertIsNotNone(text_field.internal_name)

    def test8_delete_tax_field(self):
        assert self.target_field is not None
        self.target_field.delete_object().execute_query()
