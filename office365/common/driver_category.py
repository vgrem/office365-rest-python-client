from __future__ import annotations

from enum import Enum


class DriverCategory(Enum):
    recommended = "0"
    previouslyApproved = "1"
    other = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DriverCategory"
