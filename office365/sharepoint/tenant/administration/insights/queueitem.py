from datetime import datetime

from office365.runtime.client_value import ClientValue
from typing import Optional


class InsightsQueueItem(ClientValue):
    def __init__(
        self,
        insights_completion_time: Optional[datetime] = None,
        insights_scenario: Optional[int] = None,
        item_id: Optional[int] = None,
        report_creation_time: Optional[datetime] = None,
        report_data_file_name: Optional[str] = None,
        report_id: Optional[str] = None,
        status: Optional[int] = None,
    ):
        self.insightsCompletionTime = insights_completion_time
        self.insightsScenario = insights_scenario
        self.itemId = item_id
        self.reportCreationTime = report_creation_time
        self.reportDataFileName = report_data_file_name
        self.reportId = report_id
        self.status = status

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.InsightsQueueItem"
