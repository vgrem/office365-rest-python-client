from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from office365.runtime.client_value import ClientValue


@dataclass
class SemanticSearchCrawlerEnqueueItem(ClientValue):
    ItemId: int | None = None
    ItemUrl: str | None = None
    ListId: str | None = None
    VroomId: str | None = None
    AssociateSiteId: UUID | None = None
    ItemUniqueId: UUID | None = None
    SecondsInDB: int | None = None
    SemanticSearchServiceEndPointJson: str | None = None
    SourceAction: int | None = None
    WorkItemId: UUID | None = None
