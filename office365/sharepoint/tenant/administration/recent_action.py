from __future__ import annotations

from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class TenantAdminRecentAction(ClientValue):
    adminActionId: str | None = None
    adminActionSource: int | None = None
    adminActionStatus: int | None = None
    adminActionType: int | None = None
    correlationId: UUID | None = None
    createdTime: datetime | None = None
    isPartOfBulkUpdate: bool | None = None
    key: str | None = None
    name: str | None = None
    newValue: str | None = None
    oldValue: str | None = None
    type: str | None = None
    url: str | None = None
    userEmail: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.TenantAdminRecentAction"
