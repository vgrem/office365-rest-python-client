"""Tests for SharePoint web template retrieval by enumeration, name, and type."""

from __future__ import annotations

from office365.sharepoint.webs.templates.type import WebTemplateType

from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointWebTemplates(SPTestCase):
    """Test SharePoint web template features."""

    def test_01_get_available_web_templates(self):
        """Get all available web templates."""
        templates = self.client.web.get_available_web_templates().execute_query()
        self.assertGreater(len(templates), 0)

    def test_02_get_web_template_by_name(self):
        """Get a web template by its name."""
        template_name = "GLOBAL#0"
        result = self.client.site.get_web_templates().get_by_name(template_name).get().execute_query()
        self.assertIsNotNone(result)

    def test_03_get_web_template_by_type(self):
        """Get a web template by its type."""
        result = self.client.site.get_web_templates().get_by_type(WebTemplateType.GROUP).get().execute_query()
        self.assertIsNotNone(result)
