from __future__ import annotations

from enum import Enum


class PolicySetStatus(Enum):
    unknown = "0"
    validating = "1"
    partialSuccess = "2"
    success = "3"
    error = "4"
    notAssigned = "5"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PolicySetStatus"
