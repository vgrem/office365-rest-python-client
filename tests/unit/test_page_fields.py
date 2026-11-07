"""The page-item facts the library spells once: declarations, fields, bodies, the modern rule."""

import unittest

from office365.migration.offline import offline_context
from office365.runtime.schema import TypeSchema
from office365.sharepoint.contenttypes.builtin_content_type_id import SPBuiltInContentTypeId
from office365.sharepoint.publishing.pages.coauth_state import SitePageCoAuthState
from office365.sharepoint.publishing.pages.fields import PAGE_FIELDS
from office365.sharepoint.publishing.pages.fields_data import SitePageFieldsData
from office365.sharepoint.publishing.pages.page import SitePage

#: A page content type derived from "Site Page" (the ID is hierarchical).
DERIVED_SITE_PAGE = SPBuiltInContentTypeId.SitePage + "005E10E40F8E37D94AB983A0181120EFFC"


def _page(payload: dict) -> SitePage:
    """A page read from an item payload — hydration needs a context, not a service."""
    return SitePage(offline_context()).hydrate(payload)


class TestPageFields(unittest.TestCase):
    def test_every_projected_name_is_declared(self):
        declared = set(SitePage._schema.by_attr.values())
        self.assertEqual(set(PAGE_FIELDS) - declared, set())


class TestPagePayload(unittest.TestCase):
    """A body carries what the caller filled in, not what the type declares.

    ``SitePageFieldsData`` holds four ``default_factory`` members, so serialising every
    attribute sent ``"CoAuthState": {}`` -- an empty object where a SharePoint 2019 farm wants
    an object it can read, and it answers ``property CoAuthState does not exist on type``. A
    modern farm knows the property and accepts the empty object, which is why no run against
    our tenant can show this: the defect and its fix look the same there. No 2019 lab is
    available (doc 37 V7), so the payload itself is the evidence.
    """

    def test_only_what_the_caller_set_reaches_the_body(self):
        self.assertEqual(SitePageFieldsData(Title="x").to_json(), {"Title": "x"})

    def test_a_nested_value_the_caller_filled_in_is_still_sent(self):
        # The rule drops what is empty, not what is nested: over-reaching here would break
        # every collaborative edit, silently.
        data = SitePageFieldsData(Title="x", CoAuthState=SitePageCoAuthState(IsNewSession=True))

        self.assertEqual(data.to_json(), {"Title": "x", "CoAuthState": {"IsNewSession": True}})


class TestIsModernPage(unittest.TestCase):
    def test_a_derived_site_page_content_type_is_modern_without_a_canvas(self):
        page = _page({"ContentTypeId": DERIVED_SITE_PAGE})
        self.assertTrue(page.is_modern)

    def test_a_canvas_makes_a_page_modern_whatever_its_content_type(self):
        page = _page({"ContentTypeId": "0x010108", "CanvasContent1": "<div/>"})
        self.assertTrue(page.is_modern)

    def test_a_classic_wiki_page_without_a_canvas_is_not_modern(self):
        page = _page({"ContentTypeId": "0x010108", "WikiField": "<p>wiki</p>"})
        self.assertFalse(page.is_modern)
        self.assertTrue(page.is_classic)
        self.assertEqual(page.body, "<p>wiki</p>")
        self.assertEqual(page.body_field, TypeSchema.of(SitePage).name_of("wiki"))

    def test_a_modern_page_bodies_through_its_canvas(self):
        page = _page({"ContentTypeId": DERIVED_SITE_PAGE, "CanvasContent1": "<div/>"})
        self.assertEqual(page.body, "<div/>")
        self.assertEqual(page.body_field, TypeSchema.of(SitePage).name_of("canvas_content"))
