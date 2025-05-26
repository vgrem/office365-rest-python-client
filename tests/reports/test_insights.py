from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestInsights(GraphTestCase):

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test1_list_trending(self):
        result = self.client.me.insights.trending.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test2_list_shared(self):
        result = self.client.me.insights.shared.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("Sites.Read.All", "Sites.ReadWrite.All")
    def test3_list_used(self):
        result = self.client.me.insights.used.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("User.Read", "User.Read.All", "User.ReadWrite.All")
    def test4_get_user_settings(self):
        result = self.client.me.settings.get().execute_query()
        self.assertIsNotNone(result.resource_path)
