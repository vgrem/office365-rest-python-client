from __future__ import annotations

from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class DashboardItemInfo(ClientValue):
    ItemId: int | None = None
    ListId: UUID | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None
