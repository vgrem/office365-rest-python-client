from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class RcdGroupDefinition(ClientValue):
    createdAt: datetime | None = field(default_factory=lambda: datetime.min)
    id: UUID | None = None
    name: str | None = None
    sites: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.Administration.TenantAdmin.CatalogManagement.RcdGroupDefinition"
