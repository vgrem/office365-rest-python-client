from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.adaptivecardcolumn import (
    AdaptiveCardColumn,
)
from office365.sharepoint.clientsidecomponent.padding import Padding


@dataclass
class ColumnSet(ClientValue):
    columns: ClientValueCollection[AdaptiveCardColumn] = field(
        default_factory=lambda: ClientValueCollection(AdaptiveCardColumn)
    )
    horizontal_alignment: str | None = None
    padding: Padding = field(default_factory=Padding)
