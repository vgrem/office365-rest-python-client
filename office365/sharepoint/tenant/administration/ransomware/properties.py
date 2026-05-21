from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class RansomwareProperties(ClientValue):
    activityGeneratedOn: datetime | None = None
    activityId: str | None = None
    category: int | None = None
    detectionSource: str | None = None
    driveId: str | None = None
    firstActivity: datetime | None = None
    impactedAssetLocation: str | None = None
    impactedAssetsCount: int | None = None
    impactedDocLibName: str | None = None
    impactedSiteType: int | None = None
    lastActivity: datetime | None = None
    processedStatus: int | None = None
    ransomwareDetectionReason: str | None = None
    ransomwareDetectionScore: float | None = None
    runId: str | None = None
    siteLabelId: str | None = None
    siteLabelName: str | None = None
    siteName: str | None = None
    siteOwnerName: str | None = None
    siteSubscriptionId: str | None = None
    siteUrl: str | None = None
    userName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.RansomwareProperties"
