from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class RcdGroupMetadata(ClientValue):
    createdAt: datetime | None = field(default_factory=lambda: datetime.min)
    id: UUID | None = None
    lastOperationResult: str | None = None
    name: str | None = None
    siteCount: int | None = None
    status: int | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.RcdGroupMetadata"
