from datetime import datetime
from typing import Optional

from office365.runtime.types.collections import StringCollection
from office365.sharepoint.entity import Entity


class SPTenantIBPolicyComplianceReport(Entity):

    @property
    def complete_time_in_utc(self) -> datetime:
        """Gets the CompleteTimeInUtc property"""
        return self.properties.get("CompleteTimeInUtc", datetime.min)

    @property
    def content(self) -> StringCollection:
        """Gets the Content property"""
        return self.properties.get("Content", StringCollection())

    @property
    def download_report_file_path(self) -> Optional[str]:
        """Gets the DownloadReportFilePath property"""
        return self.properties.get("DownloadReportFilePath", None)

    @property
    def incompatible_segments_pairs_content(self) -> StringCollection:
        """Gets the IncompatibleSegmentsPairsContent property"""
        return self.properties.get("IncompatibleSegmentsPairsContent", StringCollection())

    @property
    def invalid_segments_content(self) -> StringCollection:
        """Gets the InvalidSegmentsContent property"""
        return self.properties.get("InvalidSegmentsContent", StringCollection())

    @property
    def queued_time_in_utc(self) -> datetime:
        """Gets the QueuedTimeInUtc property"""
        return self.properties.get("QueuedTimeInUtc", datetime.min)

    @property
    def start_time_in_utc(self) -> datetime:
        """Gets the StartTimeInUtc property"""
        return self.properties.get("StartTimeInUtc", datetime.min)

    @property
    def state(self) -> Optional[str]:
        """Gets the State property"""
        return self.properties.get("State", None)

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.AuthPolicy.SPTenantIBPolicyComplianceReport"
