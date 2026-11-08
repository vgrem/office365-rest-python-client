from __future__ import annotations

from enum import Enum


class IngestionSource(Enum):
    unknown = "0"
    custom = "1"
    builtIn = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.IngestionSource"
