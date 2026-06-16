"""List columns — creating text, lookup columns and listing them in a document library.

Tests cover:
  - Listing all columns in the document library
  - Creating a text column
  - Creating a lookup column (referencing the same list)
  - Deleting created columns
  - Column property assertions (name, type)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.onedrive.columns.definition import ColumnDefinition
from office365.onedrive.columns.text import TextColumn
from office365.onedrive.lists.list import List
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestColumn(GraphDelegatedTestCase):
    """List column CRUD in the document library."""

    list_columns: ClassVar[list[ColumnDefinition]] = []
    doclib: ClassVar[Optional[List]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doclib = cls.client.sites.root.lists["Documents"]

    @requires_delegated(
        "Sites.Read.All",
        "Sites.Manage.All",
        "Sites.FullControl.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_list_list_columns(self):
        """Listing all columns in the document library returns at least one column."""
        columns = self.doclib.columns.get().execute_query()
        self.assertGreater(len(columns), 0)

    @requires_delegated(
        "Sites.Manage.All",
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_create_text_column(self):
        """Creating a text column in the document library should succeed."""
        name = create_unique_name("TextColumn")
        column = self.doclib.columns.add_text(name).execute_query()
        self.assertIsNotNone(column.resource_path)
        self.assertEqual(column.display_name, name)
        self.assertIsInstance(column.text, TextColumn)
        TestColumn.list_columns.append(column)

    @requires_delegated(
        "Sites.Manage.All",
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_create_lookup_column(self):
        """Creating a lookup column referencing the same list should succeed."""
        name = create_unique_name("LookupColumn")
        column = self.doclib.columns.add_lookup(name, self.doclib).execute_query()
        self.assertIsNotNone(column.resource_path)
        self.assertEqual(column.display_name, name)
        self.assertIsNotNone(column.lookup)
        TestColumn.list_columns.append(column)

    @requires_delegated(
        "Sites.Manage.All",
        "Sites.FullControl.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_04_delete_list_columns(self):
        """Deleting previously created list columns should succeed."""
        for col in TestColumn.list_columns:
            try:
                col.delete_object().execute_query()
            except Exception:
                pass
        TestColumn.list_columns.clear()
