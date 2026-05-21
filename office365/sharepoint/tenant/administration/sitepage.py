from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SPSitePage(ClientValue):
    CreatedBy: str | None = None
    CreatedDateTime: datetime | None = None
    LastModifiedDateTime: datetime | None = None
    Name: str | None = None
    Title: str | None = None
    UniqueId: UUID | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSitePage"
