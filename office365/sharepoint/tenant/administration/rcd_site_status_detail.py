from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class RcdSiteStatusDetail(ClientValue):
    applicationStatus: int | None = None
    lastUpdated: datetime | None = field(default_factory=lambda: datetime.min)
    siteId: UUID | None = None
    siteUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.RcdSiteStatusDetail"
