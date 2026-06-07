from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.publishing.pages.page import SitePage

from tests.sharepoint.sharepoint_case import SPTestCase


class TestMultilingual(SPTestCase):
    """Multilingual site features tests"""

    site_page: ClassVar[Optional[SitePage]] = None

    def test_01_is_web_multilingual(self):
        """Check if the web is multilingual"""
        web = (
            self.client.web.select(["IsMultilingual", "SupportedUILanguageIds"])
            .expand(["MultilingualSettings"])
            .get()
            .execute_query()
        )
        self.assertIsNotNone(web.is_multilingual)
        self.assertIsNotNone(web.supported_ui_language_ids)
        self.assertIsNotNone(web.multilingual_settings)

    def test_02_create_page(self):
        """Create a site page with a specific language"""
        page_title = "My Page"
        site_page = self.client.site_pages.create_page(page_title, language="en-us").execute_query()
        self.assertIsNotNone(site_page.resource_path)
        TestMultilingual.site_page = site_page

    def test_03_get_page_language(self):
        """Get the language of a site page"""
        self.assertIsNotNone(TestMultilingual.site_page)
        site_page = TestMultilingual.site_page.get().select(["Language"]).execute_query()
        self.assertIsNotNone(site_page.language)

    # The Machine Translations Service API will no longer be supported as of the end of July 2022
    # def test4_get_page_language(self):
    #    from office365.sharepoint.translation.job import TranslationJob
    #    job = TranslationJob.is_service_enabled(self.client, "en").execute_query()
    #    self.assertIsNotNone(job.value)

    # def test5_export_items_variations(self):
    #    from office365.sharepoint.translation.variations_timer_job import (
    #        VariationsTranslationTimerJob,
    #    )
    #
    #    result = VariationsTranslationTimerJob.export_items(
    #        self.client, "/sites/team/SitePages", [1, 2, 3]
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)
