from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.publishing.ruleerrordetails import RuleErrorDetails


class RuleResult(ClientValue):
    ActionToTake: Optional[str] = None
    Details: RuleErrorDetails = field(default_factory=RuleErrorDetails)
    description: Optional[str] = None
    LearnMoreLink: Optional[str] = None
    ResultCount: Optional[int] = None
    RuleType: Optional[str] = None
    Status: Optional[int] = None
    Title: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.RuleResult"
