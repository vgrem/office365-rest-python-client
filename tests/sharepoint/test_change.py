from office365.sharepoint.changes.collection import ChangeCollection
from office365.sharepoint.changes.log_item_query import ChangeLogItemQuery

from tests.sharepoint.sharepoint_case import SPTestCase


class TestChange(SPTestCase):
    def test_1_get_web_changes(self):
        result = self.client.site.root_web.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    def test_2_get_site_changes(self):
        result = self.client.site.get_changes().execute_query()
        self.assertIsInstance(result, ChangeCollection)

    def test_3_get_list_item_changes_since_token(self):
        target_list = self.client.site.root_web.default_document_library()
        query = ChangeLogItemQuery(row_limit=100)
        result = target_list.get_list_item_changes_since_token(query).execute_query()
        self.assertIsNotNone(result.value)
