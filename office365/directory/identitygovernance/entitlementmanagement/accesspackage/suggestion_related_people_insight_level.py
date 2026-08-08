from __future__ import annotations

from enum import Enum


class AccessPackageSuggestionRelatedPeopleInsightLevel(Enum):
    disabled = "0"
    count = "1"
    countAndNames = "2"
    unknownFutureValue = "3"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageSuggestionRelatedPeopleInsightLevel"
