from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.rules.definition import RulesDefinition
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


@dataclass
class RulesValidationEntryResponse(ClientValue):
    Action: int | None = None
    AISuggestionText: str | None = None
    BusinessJustification: str | None = None
    LastUpdatedDateTime: datetime | None = field(default_factory=lambda: datetime.min)
    Reviewer: ReviewerInfo = field(default_factory=ReviewerInfo)
    Rule: RulesDefinition = field(default_factory=RulesDefinition)
