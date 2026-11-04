from __future__ import annotations

from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
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
