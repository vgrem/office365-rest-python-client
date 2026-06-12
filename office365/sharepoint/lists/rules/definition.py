from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.properties import RulesProperties
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


@dataclass
class RulesDefinition(ClientValue):
    ActionForInvalidRules: str | None = None
    CategoryID: str | None = None
    CreatedByUser: ReviewerInfo = field(default_factory=ReviewerInfo)
    CreatedDateTime: str | None = None
    IsActive: bool | None = None
    IsManual: bool | None = None
    ModifiedByUser: ReviewerInfo = field(default_factory=ReviewerInfo)
    ModifiedDateTime: str | None = None
    Properties: ClientValueCollection[RulesProperties] = field(
        default_factory=lambda: ClientValueCollection(RulesProperties)
    )
    Risk: int | None = None
    RuleGroup: str | None = None
    RuleId: int | None = None
    RuleStatement: str | None = None
