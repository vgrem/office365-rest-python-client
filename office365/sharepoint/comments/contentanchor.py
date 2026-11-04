from __future__ import annotations

from datetime import time
from typing import Optional
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContentAnchor(ClientValue):
    timelineOffset: Optional[time] = None
    partitionId: str | None = None
    position: str | None = None
    uniqueId: UUID | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.ContentAnchor"
