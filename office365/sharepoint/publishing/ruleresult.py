from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.ruleerrordetails import RuleErrorDetails


class RuleResult(ClientValue):

    def __init__(
        self,
        action_to_take: str = None,
        details: RuleErrorDetails = RuleErrorDetails(),
        description: str = None,
        learn_more_link: str = None,
        result_count: int = None,
        rule_type: str = None,
        status: int = None,
        title: str = None,
    ):
        self.ActionToTake = action_to_take
        self.Details = details
        self.description = description
        self.LearnMoreLink = learn_more_link
        self.ResultCount = result_count
        self.RuleType = rule_type
        self.Status = status
        self.Title = title
