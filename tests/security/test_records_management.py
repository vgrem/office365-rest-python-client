from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestRecordsManagement(GraphDelegatedTestCase):
    @requires_delegated(
        "RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All",
        and_roles=["Security Administrator", "Security Reader"],
        or_roles=["Global Administrator"],
    )
    def test2_list_retention_event_types(self):
        """List retention event types."""
        result = self.client.security.trigger_types.retention_event_types.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # @requires_delegated(
    #    "RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All",
    #    and_roles=["Security Administrator", "Security Reader"],
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

    @requires_delegated(
        "RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All",
        and_roles=["Security Administrator", "Security Reader"],
        or_roles=["Global Administrator"],
    )
    def test4_list_retention_labels(self):
        """List retention labels."""
        result = self.client.security.labels.retention_labels.get().execute_query()
        self.assertIsNotNone(result.resource_path)
