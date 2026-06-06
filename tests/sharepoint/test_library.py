from __future__ import annotations

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSPLibrary(SPTestCase):
    """SharePoint library operations tests"""

    def test_01_get_default_library(self):
        """Get the default document library"""
        result = self.client.web.default_document_library().get().execute_query()
        self.assertIsNotNone(result.id)

    def test_02_get_default_library_url(self):
        """Get the default document library URL"""
        result = self.client.web.get_default_document_library_url().execute_query()
        self.assertIsNotNone(result.value)

    # def test3_get_files(self):
    #    lib = self.client.web.default_document_library()
    #    result = lib.get_files().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test4_get_folders(self):
    #    lib = self.client.web.default_document_library()
    #    result = lib.get_folders().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test4_reset_doc_id(self):
    #    lib = self.client.web.default_document_library()
    #    lib.reset_doc_id().execute_query()
    #    #self.assertIsNotNone(default_lib.id)

    def test_03_create_word_document(self):
        """Create a Word document and get edit link"""
        lib = self.client.web.default_document_library()
        result = lib.create_document_and_get_edit_link().execute_query()
        self.assertIsNotNone(result.value)
