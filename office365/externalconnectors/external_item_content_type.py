from __future__ import annotations

from enum import Enum


class ExternalItemContentType(Enum):
    text = "1"
    html = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.externalConnectors.ExternalItemContentType"
