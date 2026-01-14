from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.rules.userinfo import SPRuleUserInfo


class SPListRule(ClientValue):
    def __init__(
        self,
        action_params: str = None,
        action_type: int = None,
        condition: str = None,
        create_date: datetime = None,
        id_: str = None,
        is_active: bool = None,
        last_modified_by: SPRuleUserInfo = SPRuleUserInfo(),
        last_modified_date: datetime = None,
        outcome: str = None,
        owner: str = None,
        rule_template_id: str = None,
        title: str = None,
        trigger_type: int = None,
    ):
        self.ActionParams = action_params
        self.ActionType = action_type
        self.Condition = condition
        self.CreateDate = create_date
        self.ID = id_
        self.IsActive = is_active
        self.LastModifiedBy = last_modified_by
        self.LastModifiedDate = last_modified_date
        self.Outcome = outcome
        self.Owner = owner
        self.RuleTemplateId = rule_template_id
        self.Title = title
        self.TriggerType = trigger_type
