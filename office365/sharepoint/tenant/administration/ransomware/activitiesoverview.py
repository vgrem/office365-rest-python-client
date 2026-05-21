from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class TenantAdminRansomwareActivitiesOverview(ClientValue):
    categoryThresholdLimit: int | None = None
    firstActivityTime: datetime | None = None
    impactedAssetsCount: int | None = None
    lastActivityTime: datetime | None = None
    oneDriveActivityCount: int | None = None
    sharePointActivityCount: int | None = None
    totalActivitiesCount: int | None = None
    totalHighVolumeComponentActivityDetectionCount: int | None = None
    unresolvedActivitiesCount: int | None = None
    usersCount: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareActivitiesOverview"
