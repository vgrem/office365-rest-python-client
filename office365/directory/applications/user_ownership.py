from __future__ import annotations

from enum import Enum


class UserOwnership(Enum):
    none = "0"
    lawfulBasisForProcessing = "1"
    rightToAccess = "2"
    rightToBeInformed = "4"
    rightToDataPortability = "8"
    rightToObject = "16"
    rightToRectification = "32"
    rightToRestrictionOfProcessing = "64"
    rightsRelatedToAutomatedDecisionMaking = "128"
    unknownFutureValue = "256"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserOwnership"
