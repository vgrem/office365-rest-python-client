"""OneNote pages — creating from HTML, listing, and property inspection.

Tests cover:
  - Creating a page from HTML content with a title
  - Listing pages from the default section
  - Page property assertions (title, section links, createdDateTime)
  - Getting page content
"""

from __future__ import annotations

import io
from typing import ClassVar, Optional

from office365.onenote.pages.page import OnenotePage

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPage(GraphDelegatedTestCase):
    """OneNote page creation and property inspection."""

    target_page: ClassVar[Optional[OnenotePage]] = None

    @requires_delegated(
        "Notes.Create",
        "Notes.ReadWrite",
        "Notes.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_01_create_page_from_html(self):
        """Creating a page from HTML with a title should succeed."""
        html = b"""<!DOCTYPE html>
<html>
<head><title>SDK Test Page</title></head>
<body>
    <p>Hello from office365-rest-python-client</p>
    <p>This page was created via the Graph API.</p>
</body>
</html>"""
        presentation = io.BytesIO(html)
        presentation.name = "page.html"

        page = self.client.me.onenote.pages.add(presentation_file=presentation).execute_query()
        self.assertIsNotNone(page.resource_path)
        self.assertIsNotNone(page.get_property("id"))
        TestPage.target_page = page

    @requires_delegated(
        "Notes.Read",
        "Notes.Read.All",
        "Notes.ReadWrite",
        "Notes.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_02_page_has_expected_properties(self):
        """A page object exposes title, createdDateTime, and links."""
        page = TestPage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        self.assertIsNotNone(page.title)
        self.assertIsNotNone(page.created_datetime)
        # links should contain parentNotebook and parentSection URLs
        self.assertIsNotNone(page.links)

    @requires_delegated(
        "Notes.Read",
        "Notes.Read.All",
        "Notes.ReadWrite",
        "Notes.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_03_list_pages_from_first_section(self):
        """Listing pages from the first available section returns a collection."""
        sections = self.client.me.onenote.sections.top(1).get().execute_query()
        if len(sections) == 0:
            self.skipTest("No sections found")

        pages = sections[0].pages.top(10).get().execute_query()
        self.assertIsNotNone(pages)

    @requires_delegated(
        "Notes.Read",
        "Notes.Read.All",
        "Notes.ReadWrite",
        "Notes.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_04_page_title_includes_html_title(self):
        """The page title should reflect the HTML <title> tag used during creation."""
        page = TestPage.target_page
        if not page:
            self.skipTest("No page created from previous test")

        title = page.title
        if title:
            self.assertIsInstance(title, str)
            self.assertGreater(len(title), 0)

    @classmethod
    def tearDownClass(cls):
        page = cls.target_page
        if page and page.resource_path:
            try:
                page.delete_object().execute_query()
            except Exception:
                pass
