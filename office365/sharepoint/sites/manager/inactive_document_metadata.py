from __future__ import annotations

from dataclasses import field
from datetime import datetime
from uuid import UUID

from office365.runtime.client_value import ClientValue


class InactiveDocumentMetadata(ClientValue):
    Description: str | None = None
    LastAccessDate: datetime | None = field(default_factory=lambda: datetime.min)
    LastActivityTimestamp: datetime | None = field(default_factory=lambda: datetime.min)
    ListId: UUID | None = None
    ListItemId: str | None = None
    Path: str | None = None
    PictureThumbnailUrl: str | None = None
    Title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SiteManager.InactiveDocumentMetadata"
