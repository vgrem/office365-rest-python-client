from datetime import datetime
from typing import Optional

from office365.sharepoint.entity import Entity


class SPTenantIBInsightsReportMetadata(Entity):
    """ """

    @property
    def complete_time_in_utc(self) -> datetime:
        """Gets the CompleteTimeInUtc property"""
        return self.properties.get("CompleteTimeInUtc", None)

    @property
    def queued_time_in_utc(self) -> datetime:
        """Gets the QueuedTimeInUtc property"""
        return self.properties.get("QueuedTimeInUtc", None)

    @property
    def start_time_in_utc(self) -> datetime:
        """Gets the StartTimeInUtc property"""
        return self.properties.get("StartTimeInUtc", None)

    @property
    def state(self) -> Optional[str]:
        """Gets the State property"""
        return self.properties.get("State", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Insights.SPTenantIBInsightsReportMetadata"
