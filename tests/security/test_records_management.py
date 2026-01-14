from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestRecordsManagement(GraphTestCase):
    @requires_delegated_permission("RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All")
    def test2_list_retention_event_types(self):
        result = self.client.security.trigger_types.retention_event_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # @requires_delegated_permission(
    #    "RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All"
    # )
    # def test3_create_retention_label(self):
    #    result = self.client.security.labels.retention_labels.add(
    #        "Retain 1 year",
    #        RetentionTrigger.dateLabeled,
    #        RetentionDurationInDays(365),
    #        BehaviorDuringRetentionPeriod.retainAsRecord,
    #        DefaultRecordBehavior.startLocked,
    #        ActionAfterRetentionPeriod.delete,
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All")
    def test4_list_retention_labels(self):
        result = self.client.security.labels.retention_labels.get().execute_query()
        self.assertIsNotNone(result.resource_path)
