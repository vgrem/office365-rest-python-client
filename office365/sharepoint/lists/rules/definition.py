from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.properties import RulesProperties
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


class RulesDefinition(ClientValue):
    def __init__(
        self,
        action_for_invalid_rules: Optional[str] = None,
        category_id: Optional[str] = None,
        created_by_user: ReviewerInfo = ReviewerInfo(),
        created_date_time: Optional[str] = None,
        is_active: Optional[bool] = None,
        is_manual: Optional[bool] = None,
        modified_by_user: Optional[ReviewerInfo] = None,
        modified_date_time: Optional[str] = None,
        properties: ClientValueCollection[RulesProperties] = ClientValueCollection(RulesProperties),
        risk: Optional[int] = None,
        rule_group: Optional[str] = None,
        rule_id: Optional[int] = None,
        rule_statement: Optional[str] = None,
    ):
        self.action_for_invalid_rules = action_for_invalid_rules
        self.category_id = category_id
        self.created_by_user = created_by_user
        self.created_date_time = created_date_time
        self.is_active = is_active
        self.is_manual = is_manual
        self.modified_by_user = modified_by_user
        self.modified_date_time = modified_date_time
        self.properties = properties
        self.risk = risk
        self.rule_group = rule_group
        self.rule_id = rule_id
        self.rule_statement = rule_statement
