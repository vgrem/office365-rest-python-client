from __future__ import annotations

from enum import Enum


class PlaceFeatureEnablement(Enum):
    unknown = "0"
    enabled = "1"
    disabled = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PlaceFeatureEnablement"
