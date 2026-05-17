from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.lists.rules.userinfo import SPRuleUserInfo


class SPListRule(ClientValue):
    def __init__(
        self,
        action_params: Optional[str] = None,
        action_type: Optional[int] = None,
        condition: Optional[str] = None,
        create_date: Optional[datetime] = None,
        id_: Optional[str] = None,
        is_active: Optional[bool] = None,
        last_modified_by: SPRuleUserInfo = SPRuleUserInfo(),
        last_modified_date: Optional[datetime] = None,
        outcome: Optional[str] = None,
        owner: Optional[str] = None,
        rule_template_id: Optional[str] = None,
        title: Optional[str] = None,
        trigger_type: Optional[int] = None,
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
