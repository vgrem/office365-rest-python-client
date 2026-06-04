"""Tests for Microsoft Graph OneNote Sections API."""

from typing import Optional

from office365.onenote.notebooks.notebook import Notebook
from office365.onenote.sections.section import OnenoteSection
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSection(GraphDelegatedTestCase):
    """Tests for OneNote sections."""

    target_notebook: Optional[Notebook] = None
    target_section: Optional[OnenoteSection] = None

    @requires_delegated(
        "Notes.Read", "Notes.Read.All", "Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"]
    )
    def test1_list_sections(self):
        """List all OneNote sections."""
        result = self.client.me.onenote.sections.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test2_create_section(self):
        """Create a section in a new notebook."""
        notebook_name = create_unique_name("Test Notebook")
        notebook = self.client.me.onenote.notebooks.add(notebook_name).execute_query()
        self.assertIsNotNone(notebook.resource_path)
        TestSection.target_notebook = notebook

        name = create_unique_name("Test Section")
        section = notebook.sections.add(displayName=name).execute_query()
        self.assertIsNotNone(section.resource_path)
        TestSection.target_section = section

    @requires_delegated("Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test3_update_section(self):
        """Update a section display name."""
        assert TestSection.target_section is not None, "Section must be created"
        section = TestSection.target_section
        new_name = create_unique_name("Updated Section")
        section.set_property("displayName", new_name).update().execute_query()
        self.assertEqual(section.display_name, new_name)

    @requires_delegated("Notes.ReadWrite", "Notes.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test4_delete_notebook(self):
        """Delete the test notebook (cascades to section)."""
        assert TestSection.target_notebook is not None, "Notebook must be created"
        TestSection.target_notebook.delete_object().execute_query()
