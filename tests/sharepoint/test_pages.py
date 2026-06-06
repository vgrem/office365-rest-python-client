from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.files.file import File
from office365.sharepoint.lists.list import List

from tests import create_unique_name
from tests.sharepoint.sharepoint_case import SPTestCase


class TestPages(SPTestCase):
    """SharePoint pages tests"""

    pages_list: ClassVar[Optional[List]] = None
    target_file: ClassVar[Optional[File]] = None

    def test_01_ensure_site_pages_library(self):
        """Ensure site pages library exists"""
        pages_list = self.client.web.lists.ensure_site_pages_library().execute_query()
        self.assertIsNotNone(pages_list.resource_path)
        TestPages.pages_list = pages_list

    def test_02_create_wiki_page(self):
        """Create a wiki page"""
        self.assertIsNotNone(TestPages.pages_list)
        page_name = create_unique_name("WikiPage") + ".aspx"
        file = TestPages.pages_list.create_wiki_page(page_name, "Wiki content").execute_query()
        self.assertIsNotNone(file.resource_path)
        TestPages.target_file = file

    def test_03_delete_page(self):
        """Delete a page"""
        self.assertIsNotNone(TestPages.target_file)
        TestPages.target_file.delete_object().execute_query()
