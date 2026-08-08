from __future__ import annotations

from enum import Enum


class UserFeedbackRating(Enum):
    notRated = "0"
    bad = "1"
    poor = "2"
    fair = "3"
    good = "4"
    excellent = "5"
    unknownFutureValue = "6"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.UserFeedbackRating"
