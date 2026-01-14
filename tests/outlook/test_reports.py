from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestOutlookReports(GraphTestCase):
    @requires_delegated_permission("Reports.Read.All")
    def test1_get_email_activity_counts(self):
        result = self.client.reports.get_email_activity_counts("D90").execute_query()
        self.assertIsNotNone(result.value)

    def test2_get_m365_app_user_counts(self):
        result = self.client.reports.get_m365_app_user_counts("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("Reports.Read.All")
    def test3_get_email_activity_user_detail(self):
        result = self.client.reports.get_email_activity_user_detail("D7").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("Reports.Read.All")
    def test4_get_mailbox_usage_storage(self):
        result = self.client.reports.get_mailbox_usage_storage("D30").execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated_permission("Reports.Read.All")
    def test5_get_mailbox_usage_mailbox_counts(self):
        result = self.client.reports.get_mailbox_usage_mailbox_counts("D90").execute_query()
        self.assertIsNotNone(result.value)
