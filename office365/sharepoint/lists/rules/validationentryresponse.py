from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.rules.definition import RulesDefinition
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


@dataclass
class RulesValidationEntryResponse(ClientValue):
    action: Optional[int] = None
    ai_suggestion_text: Optional[str] = None
    business_justification: Optional[str] = None
    last_updated_date_time: datetime = datetime.min
    reviewer: ReviewerInfo = field(default_factory=ReviewerInfo)
    rule: RulesDefinition = field(default_factory=RulesDefinition)
