"""Tests for Microsoft Graph OneNote Notebooks API."""

from typing import Optional

from office365.onenote.notebooks.notebook import Notebook
from office365.onenote.sections.section import OnenoteSection
from tests import create_unique_name
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestNotebook(GraphDelegatedTestCase):
    """Tests for OneNote notebooks."""

    target_notebook: Optional[Notebook] = None
    target_section: Optional[OnenoteSection] = None

    @requires_delegated_permission_or_role(
        "Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All", roles=["Global Administrator"]
    )
    def test1_create_notebook(self):
        """Create a new OneNote notebook."""
        notebook_name = create_unique_name("My Private notebook")
        result = self.client.me.onenote.notebooks.add(notebook_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestNotebook.target_notebook = result

    @requires_delegated_permission_or_role("Notes.Create", roles=["Global Administrator"])
    def test2_list_notebooks(self):
        """List all OneNote notebooks."""
        result = self.client.me.onenote.notebooks.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role(
        "Notes.Create",
        "Notes.Read",
        "Notes.Read.All",
        "Notes.ReadWrite",
        "Notes.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test3_get_recent_notebooks(self):
        """Get recent OneNote notebooks."""
        result = self.client.me.onenote.notebooks.get_recent_notebooks().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission_or_role(
        "Notes.Create", "Notes.ReadWrite", "Notes.ReadWrite.All", roles=["Global Administrator"]
    )
    def test4_create_section(self):
        """Create a section within the notebook."""
        notebook = TestNotebook.target_notebook
        assert notebook is not None
        name = create_unique_name("Section name")
        result = notebook.sections.add(displayName=name).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestNotebook.target_section = result
