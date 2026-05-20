from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.properties import RulesProperties
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


@dataclass
class RulesDefinition(ClientValue):
    action_for_invalid_rules: Optional[str] = None
    category_id: Optional[str] = None
    created_by_user: ReviewerInfo = field(default_factory=ReviewerInfo)
    created_date_time: Optional[str] = None
    is_active: Optional[bool] = None
    is_manual: Optional[bool] = None
    modified_by_user: Optional[ReviewerInfo] = None
    modified_date_time: Optional[str] = None
    properties: ClientValueCollection[RulesProperties] = field(
        default_factory=lambda: ClientValueCollection(RulesProperties)
    )
    risk: Optional[int] = None
    rule_group: Optional[str] = None
    rule_id: Optional[int] = None
    rule_statement: Optional[str] = None
