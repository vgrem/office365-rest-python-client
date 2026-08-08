from __future__ import annotations

from enum import Enum


class ApproverInformationVisibility(Enum):
    default = "0"
    notVisible = "1"
    visible = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApproverInformationVisibility"
