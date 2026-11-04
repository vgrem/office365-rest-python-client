from dataclasses import field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.sharepoint.lists.rules.userinfo import SPRuleUserInfo


@value
class SPListRule(ClientValue):
    ActionParams: Optional[str] = None
    ActionType: Optional[int] = None
    Condition: Optional[str] = None
    CreateDate: Optional[datetime] = None
    ID: Optional[str] = None
    IsActive: Optional[bool] = None
    LastModifiedBy: SPRuleUserInfo = field(default_factory=SPRuleUserInfo)
    LastModifiedDate: Optional[datetime] = None
    Outcome: Optional[str] = None
    Owner: Optional[str] = None
    RuleTemplateId: Optional[str] = None
    Title: Optional[str] = None
    TriggerType: Optional[int] = None
