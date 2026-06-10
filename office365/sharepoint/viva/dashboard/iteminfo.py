from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class DashboardItemInfo(ClientValue):
    ItemId: int | None = None
    ListId: UUID | None = None
    SiteId: UUID | None = None
    WebId: UUID | None = None
