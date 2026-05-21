from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAdminRansomwareEvent(ClientValue):
    assignedTo: str | None = None
    category: int | None = None
    categoryThresholdLimit: int | None = None
    classification: int | None = None
    consolidatedReportLocation: str | None = None
    createdTime: datetime | None = None
    eventId: UUID | None = None
    firstOccurrence: datetime | None = None
    investigationState: int | None = None
    lastOccurrence: datetime | None = None
    lastUpdatedTime: datetime | None = None
    severity: int | None = None
    status: int | None = None
    tagId: str | None = None
    totalHighVolumeComponentActivityDetectionCount: int | None = None
    updatedBy: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEvent"
