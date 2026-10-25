"""The page-item facts the library spells once: declarations, fields, bodies, the modern rule."""

import unittest

from office365.sharepoint.contenttypes.builtin_content_type_id import SPBuiltInContentTypeId
from office365.sharepoint.fields.builtin_field_name import SPBuiltInFieldName
from office365.sharepoint.publishing.pages.fields import BODY_FIELDS, PAGE_FIELDS, is_modern_page
from office365.sharepoint.publishing.pages.page import SitePage

#: A page content type derived from "Site Page" (the ID is hierarchical).
DERIVED_SITE_PAGE = SPBuiltInContentTypeId.SitePage + "005E10E40F8E37D94AB983A0181120EFFC"


class TestSitePageDeclarations(unittest.TestCase):
    def test_both_body_spellings_are_declared(self):
        # A wire name may be declared only once per class: the later marker wins and
        # silently leaves the earlier getter undeclared (unselectable, unrenderable).
        self.assertEqual(SitePage.odata_name("canvas_content"), "CanvasContent1")
        self.assertEqual(SitePage.odata_name("layout_web_parts_content"), "LayoutWebpartsContent")

    def test_a_hydrated_page_answers_the_body_properties(self):
        page = SitePage(None).hydrate({"CanvasContent1": "<div/>", "LayoutWebpartsContent": "<div>l</div>"})
        self.assertEqual(page.canvas_content, "<div/>")
        self.assertEqual(page.layout_web_parts_content, "<div>l</div>")

    def test_the_item_columns_are_declared_on_the_type(self):
        # A page is read from its library's items, so its type declares what an item
        # answers: hydration is by declared name, and a name nobody declares is a
        # property nobody can read off the model.
        self.assertEqual(SitePage.odata_name("file_leaf_ref"), SPBuiltInFieldName.FileLeafRef)
        self.assertEqual(SitePage.odata_name("wiki"), "WikiField")
        self.assertEqual(SitePage.odata_name("moderation_status"), "OData__ModerationStatus")

    def test_a_hydrated_page_answers_the_item_columns(self):
        page = SitePage(None).hydrate(
            {"FileLeafRef": "x.aspx", "WikiField": "<div>wiki</div>", "OData__ModerationStatus": 0}
        )
        self.assertEqual(page.file_leaf_ref, "x.aspx")
        self.assertEqual(page.wiki, "<div>wiki</div>")
        self.assertEqual(page.moderation_status, 0)


class TestPageFields(unittest.TestCase):
    def test_every_projected_name_is_declared(self):
        declared = set(SitePage._schema.by_attr.values())
        self.assertEqual(set(PAGE_FIELDS) - declared, set())

    def test_the_page_type_spells_the_file_name_differently(self):
        # Why the projection reads the item column: the entity's own spelling is not it.
        self.assertEqual(SitePage.odata_name("file_name"), "FileName")
        self.assertNotEqual(SitePage.odata_name("file_name"), SPBuiltInFieldName.FileLeafRef)

    def test_the_projection_names_each_field_once(self):
        self.assertEqual(len(PAGE_FIELDS), len(set(PAGE_FIELDS)))

    def test_the_body_fields_are_derived_from_the_type(self):
        self.assertEqual(BODY_FIELDS, (SitePage.odata_name("canvas_content"), SitePage.odata_name("wiki")))


class TestIsModernPage(unittest.TestCase):
    def test_a_derived_site_page_content_type_is_modern_without_a_canvas(self):
        self.assertTrue(is_modern_page(DERIVED_SITE_PAGE, None))

    def test_a_canvas_makes_a_page_modern_whatever_its_content_type(self):
        self.assertTrue(is_modern_page("0x010108", "<div/>"))

    def test_a_classic_wiki_page_without_a_canvas_is_not_modern(self):
        self.assertFalse(is_modern_page("0x010108", None))
