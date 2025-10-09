from datetime import datetime

from office365.runtime.client_value import ClientValue


class InsightsQueueItem(ClientValue):

    def __init__(
        self,
        insights_completion_time: datetime = None,
        insights_scenario: int = None,
        item_id: int = None,
        report_creation_time: datetime = None,
        report_data_file_name: str = None,
        report_id: str = None,
        status: int = None,
    ):
        self.insightsCompletionTime = insights_completion_time
        self.insightsScenario = insights_scenario
        self.itemId = item_id
        self.reportCreationTime = report_creation_time
        self.reportDataFileName = report_data_file_name
        self.reportId = report_id
        self.status = status

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsQueueItem"
