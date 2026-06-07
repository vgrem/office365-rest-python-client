"""Tests for SharePoint document set operations (create and delete)."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.documentmanagement.document_set import DocumentSet
from office365.sharepoint.lists.list import List

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointDocumentSet(SPTestCase):
    """Tests for SharePoint document set lifecycle operations."""

    target_lib: ClassVar[Optional[List]] = None
    target_doc_set: ClassVar[Optional[DocumentSet]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        list_title = create_unique_name("Archive Documents")
        cls.target_lib = cls.client.web.lists.add_library(list_title).execute_query()

    @classmethod
    def tearDownClass(cls):
        target = cls.target_lib
        if not target:
            return
        target.delete_object().execute_query()

    def test_01_create_document_set(self):
        """Create a document set in the target library."""
        doc_set_title = create_unique_name("DocSet N")
        target = TestSharePointDocumentSet.target_lib
        if not target:
            self.skipTest("No resource from previous test")
        doc_set = DocumentSet.create(self.client, target.root_folder, doc_set_title).execute_query()
        self.assertEqual(doc_set.name, doc_set_title)
        self.assertIsNotNone(doc_set.resource_path)
        TestSharePointDocumentSet.target_doc_set = doc_set

    def test_02_delete_document_set(self):
        """Delete the created document set."""
        target = TestSharePointDocumentSet.target_doc_set
        if not target:
            self.skipTest("No resource from previous test")
        target.delete_object().execute_query()
