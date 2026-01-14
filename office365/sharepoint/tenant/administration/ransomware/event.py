from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TenantAdminRansomwareEvent(ClientValue):
    def __init__(
        self,
        assigned_to: str = None,
        category: int = None,
        category_threshold_limit: int = None,
        classification: int = None,
        consolidated_report_location: str = None,
        created_time: datetime = None,
        event_id: UUID = None,
        first_occurrence: datetime = None,
        investigation_state: int = None,
        last_occurrence: datetime = None,
        last_updated_time: datetime = None,
        severity: int = None,
        status: int = None,
        tag_id: str = None,
        total_high_volume_component_activity_detection_count: int = None,
        updated_by: str = None,
    ):
        self.assignedTo = assigned_to
        self.category = category
        self.categoryThresholdLimit = category_threshold_limit
        self.classification = classification
        self.consolidatedReportLocation = consolidated_report_location
        self.createdTime = created_time
        self.eventId = event_id
        self.firstOccurrence = first_occurrence
        self.investigationState = investigation_state
        self.lastOccurrence = last_occurrence
        self.lastUpdatedTime = last_updated_time
        self.severity = severity
        self.status = status
        self.tagId = tag_id
        self.totalHighVolumeComponentActivityDetectionCount = total_high_volume_component_activity_detection_count
        self.updatedBy = updated_by

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEvent"
