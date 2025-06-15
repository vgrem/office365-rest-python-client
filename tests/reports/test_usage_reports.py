from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestUsageReports(GraphTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestUsageReports, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated_permission("PartnerBilling.Read.All")
    def test1_billed_usage_export(self):
        result = self.client.reports.partners.billing.usage.billed.export(
            "G016907411"
        ).execute_query()
        self.assertIsNotNone(result.value)
