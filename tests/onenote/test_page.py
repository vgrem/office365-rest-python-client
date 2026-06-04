"""Tests for Microsoft Graph OneNote Pages API."""

import io
from typing import Optional

from office365.onenote.pages.page import OnenotePage
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPage(GraphDelegatedTestCase):
    """Tests for OneNote pages."""

    target_page: Optional[OnenotePage] = None

    @requires_delegated("Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test1_create_page(self):
        """Create a new OneNote page from HTML."""
        html_content = b"""<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <p>Hello from office365-rest-python-client</p>
    <p>This page was created via the Graph API.</p>
</body>
</html>"""
        presentation = io.BytesIO(html_content)
        presentation.name = "page.html"

        page = self.client.me.onenote.pages.add(presentation_file=presentation).execute_query()
        self.assertIsNotNone(page.resource_path)
        TestPage.target_page = page

    @requires_delegated(
        "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"]
    )
    def test2_list_pages(self):
        """List OneNote pages from the first section."""
        sections = self.client.me.onenote.sections.top(1).get().execute_query()
        assert len(sections) > 0, "No sections found"
        my_pages = sections[0].pages.get().top(10).execute_query()
        self.assertIsNotNone(my_pages.resource_path)
