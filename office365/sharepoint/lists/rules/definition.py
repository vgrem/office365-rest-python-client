from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.rules.properties import RulesProperties
from office365.sharepoint.lists.rules.reviewinfo import ReviewerInfo


class RulesDefinition(ClientValue):

    def __init__(
        self,
        action_for_invalid_rules: str = None,
        category_id: str = None,
        created_by_user: ReviewerInfo = ReviewerInfo(),
        created_date_time: str = None,
        is_active: bool = None,
        is_manual: bool = None,
        modified_by_user: ReviewerInfo = None,
        modified_date_time: str = None,
        properties: ClientValueCollection[RulesProperties] = ClientValueCollection(RulesProperties),
        risk: int = None,
        rule_group: str = None,
        rule_id: int = None,
        rule_statement: str = None,
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
