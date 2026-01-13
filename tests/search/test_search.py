from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestSearchOneDrive(GraphTestCase):
    def test1_search_files(self):
        result = self.client.search.query_drive_items("Guide.docx").execute_query()
        self.assertIsNotNone(result.value)

    def test2_search_messages(self):
        result = self.client.search.query_messages("Jon Doe").execute_query()
        self.assertIsNotNone(result.value)

    # def test3_search_events(self):
    #    result = self.client.search.query_events("Jon Doe").execute_query()
    #    self.assertIsNotNone(result.value)

    def test4_search_list_items(self):
        result = self.client.search.query_list_items("Guide").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("People.Read")
    def test5_search_people_by_name(self):
        result = self.client.search.query_peoples("John").execute_query()
        self.assertIsNotNone(result.value)

    def test6_search_sites(self):
        result = self.client.search.query_sites("team").execute_query()
        self.assertIsNotNone(result.value)

    # @requires_delegated_permission(
    #    "Chat.Read", "Chat.ReadWrite", "ChannelMessage.Read.All"
    # )
    # def test7_search_chat_messages(self):
    #    result = self.client.search.query_chat_messages("message").execute_query()
    #    self.assertIsNotNone(result.value)
