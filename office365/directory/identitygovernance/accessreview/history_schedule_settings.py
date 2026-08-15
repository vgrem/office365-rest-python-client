from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.mail.patterned_recurrence import PatternedRecurrence
from office365.runtime.client_value import ClientValue


@dataclass
class AccessReviewHistoryScheduleSettings(ClientValue):
    recurrence: PatternedRecurrence = field(default_factory=PatternedRecurrence)
    reportRange: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessReviewHistoryScheduleSettings"
