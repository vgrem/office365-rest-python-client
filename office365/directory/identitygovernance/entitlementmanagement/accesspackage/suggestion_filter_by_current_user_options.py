from __future__ import annotations

from enum import Enum


class AccessPackageSuggestionFilterByCurrentUserOptions(Enum):
    none = "0"
    relatedPeopleAssignments = "1"
    assignmentHistory = "2"
    unknownFutureValue = "4"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSuggestionFilterByCurrentUserOptions"
