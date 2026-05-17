from office365.onenote.sections.section import OnenoteSection
from tests.graph_case import GraphTestCase


class TestSection(GraphTestCase):
    target_section: OnenoteSection = None

    def test2_list_sections(self):
        result = self.client.me.onenote.sections.get().execute_query()
        self.assertIsNotNone(result.resource_path)
