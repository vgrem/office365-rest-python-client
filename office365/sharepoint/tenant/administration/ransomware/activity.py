from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAdminRansomwareActivity(ClientValue):
    activityGeneratedOn: datetime | None = None
    activityId: str | None = None
    assignedTo: str | None = None
    category: int | None = None
    classification: int | None = None
    createdTime: datetime | None = None
    detectionSource: str | None = None
    driveId: str | None = None
    eventId: str | None = None
    firstActivity: datetime | None = None
    impactedAssetLocation: str | None = None
    impactedAssets: str | None = None
    impactedAssetsCount: int | None = None
    impactedAssetsUserCount: int | None = None
    impactedDocLibName: str | None = None
    investigationState: int | None = None
    lastActivity: datetime | None = None
    lastUpdatedTime: datetime | None = None
    processedStatus: int | None = None
    ransomwareDetectionReason: str | None = None
    RansomwareDetectionScore: float | None = None
    runId: UUID | None = None
    siteId: UUID | None = None
    siteName: str | None = None
    siteOwner: str | None = None
    siteType: int | None = None
    siteUrl: str | None = None
    status: int | None = None
    syncStatus: int | None = None
    tagId: str | None = None
    updatedBy: str | None = None
    userName: str | None = None
    webId: UUID | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareActivity"
