from office365.sharepoint.webs.templates.type import WebTemplateType
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointWebTemplates(SPTestCase):
    def test1_get_available_web_templates(self):
        templates = self.client.web.get_available_web_templates().execute_query()
        self.assertGreater(len(templates), 0)

    def test4_get_web_template_by_name(self):
        template_name = "GLOBAL#0"
        result = self.client.site.get_web_templates().get_by_name(template_name).get().execute_query()
        self.assertIsNotNone(result)

    def test4_get_web_template_by_type(self):
        result = self.client.site.get_web_templates().get_by_type(WebTemplateType.GROUP).get().execute_query()
        self.assertIsNotNone(result)
