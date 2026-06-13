from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue


class CommonMoveJob(ClientValue):
    IsContentMoved: bool | None = None
    LastModified: datetime | None = field(default_factory=lambda: datetime.min)
    StartedDateInUtc: datetime | None = field(default_factory=lambda: datetime.min)
    StateName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MultiGeo.Service.CommonMoveJob"
