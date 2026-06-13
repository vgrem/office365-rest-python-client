from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class NewsNotificationUpdatePayload(ClientValue):
    ActivityId: UUID | None = None
    ActorName: str | None = None
    ActorObjectId: UUID | None = None
    EventData: dict | None = field(default_factory=dict)
    EventType: str | None = None
    ListId: UUID | None = None
    ListItemUniqueId: UUID | None = None
    PageTitle: str | None = None
    PageUrl: str | None = None
    SiteId: UUID | None = None
    SiteName: str | None = None
    Timestamp: datetime | None = field(default_factory=lambda: datetime.min)
    WebId: UUID | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.News.NewsNotificationUpdatePayload"
