from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class TenantAdminRansomwareEventSiteRestorePoint(ClientValue):
    ransomwareEventId: UUID | None = None
    restorePointId: UUID | None = None
    restorePointState: int | None = None
    restorePointTimeUtc: datetime | None = field(default_factory=lambda: datetime.min)
    restorePointType: str | None = None
    siteId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRansomwareEventSiteRestorePoint"
