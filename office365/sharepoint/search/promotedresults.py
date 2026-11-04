from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class PromotedResults(ClientValue):
    Description: str | None = None
    IsVisual: bool | None = None
    LastModifiedTime: datetime | None = None
    Title: str | None = None
    Url: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.PromotedResults"
