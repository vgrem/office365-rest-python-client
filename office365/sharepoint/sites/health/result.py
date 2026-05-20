from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteHealthResult(ClientValue):
    """Specifies the result of running a site collection sitehealth rule.

    Fields:
        MessageAsText: Specifies a summary of the results of running a site collection sitehealth rule.
        RuleHelpLink: Specifies a hyperlink to help information about the site collection sitehealth rule.
        RuleId: Specifies the unique identifier of the site collection sitehealth rule.
    """

    MessageAsText: str | None = None
    RuleHelpLink: str | None = None
    RuleId: str | None = None
    RuleIsRepairable: Optional[bool] = None
    RuleName: Optional[str] = None
    Status: Optional[int] = None
    TimeStamp: Optional[datetime] = None

    @property
    def entity_type_name(self):
        return "SP.SiteHealth.SiteHealthResult"
