from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TenantAdminRansomwareEvent(ClientValue):
    def __init__(
        self,
        assigned_to: Optional[str] = None,
        category: Optional[int] = None,
        category_threshold_limit: Optional[int] = None,
        classification: Optional[int] = None,
        consolidated_report_location: Optional[str] = None,
        created_time: Optional[datetime] = None,
        event_id: Optional[UUID] = None,
        first_occurrence: Optional[datetime] = None,
        investigation_state: Optional[int] = None,
        last_occurrence: Optional[datetime] = None,
        last_updated_time: Optional[datetime] = None,
        severity: Optional[int] = None,
        status: Optional[int] = None,
        tag_id: Optional[str] = None,
        total_high_volume_component_activity_detection_count: Optional[int] = None,
        updated_by: Optional[str] = None,
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
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEvent"
