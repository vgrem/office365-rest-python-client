from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.ruleerrordetails import RuleErrorDetails


class RuleResult(ClientValue):
    def __init__(
        self,
        action_to_take: Optional[str] = None,
        details: RuleErrorDetails = RuleErrorDetails(),
        description: Optional[str] = None,
        learn_more_link: Optional[str] = None,
        result_count: Optional[int] = None,
        rule_type: Optional[str] = None,
        status: Optional[int] = None,
        title: Optional[str] = None,
    ):
        self.ActionToTake = action_to_take
        self.Details = details
        self.description = description
        self.LearnMoreLink = learn_more_link
        self.ResultCount = result_count
        self.RuleType = rule_type
        self.Status = status
        self.Title = title

    @property
    def entity_type_name(self):
        return "SP.Publishing.RuleResult"
