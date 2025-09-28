from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.rules.definition import RulesDefinition
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


class RulesValidationEntryResponse(ClientValue):

    def __init__(
        self,
        action: int = None,
        ai_suggestion_text: str = None,
        business_justification: str = None,
        last_updated_date_time: datetime = datetime.min,
        reviewer: ReviewerInfo = ReviewerInfo(),
        rule: RulesDefinition = RulesDefinition(),
    ):
        self.action = action
        self.ai_suggestion_text = ai_suggestion_text
        self.business_justification = business_justification
        self.last_updated_date_time = last_updated_date_time
        self.reviewer = reviewer
        self.rule = rule
