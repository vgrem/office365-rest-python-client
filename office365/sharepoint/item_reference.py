from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ItemReference(ClientValue):
    SiteId: UUID | None = None
    Type: str | None = None
    WebId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.EmployeeEngagement.ItemReference"
