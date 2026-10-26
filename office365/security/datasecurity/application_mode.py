from __future__ import annotations

from enum import Enum


class ApplicationMode(Enum):
    manual = "0"
    automatic = "1"
    recommended = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationMode"
