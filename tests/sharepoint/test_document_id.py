"""Tests for SharePoint document ID service operations."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.lists.list import List

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointDocumentId(SPTestCase):
    """Tests for SharePoint document ID operations."""

    target_lib: ClassVar[Optional[List]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_lib = cls.client.web.default_document_library()

    def test_01_get_service(self):
        """Get the document ID service."""
        result = self.client.document_id.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test2_ensure_doc_id_feature(self):
    #    result = self.client.site.features.add(
    #        KnownFeaturesList.DocId, False, FeatureDefinitionScope.Farm
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)
