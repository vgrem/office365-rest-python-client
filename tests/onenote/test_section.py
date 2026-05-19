"""Tests for Microsoft Graph OneNote Sections API."""

from typing import Optional

from office365.onenote.sections.section import OnenoteSection
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSection(GraphDelegatedTestCase):
    """Tests for OneNote sections."""

    target_section: Optional[OnenoteSection] = None

    @requires_delegated(
        "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test1_list_sections(self):
        """List all OneNote sections."""
        result = self.client.me.onenote.sections.get().execute_query()
        self.assertIsNotNone(result.resource_path)
