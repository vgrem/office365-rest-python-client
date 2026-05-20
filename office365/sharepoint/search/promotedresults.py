from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.runtime.client_value import ClientValue


@dataclass
class PromotedResults(ClientValue):
    Description: str | None = None
    IsVisual: bool | None = None
    LastModifiedTime: datetime | None = None
    Title: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResults"
