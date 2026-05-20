from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPRuleAction(ClientValue):
    action_params: Optional[dict] = None
    action_type: Optional[int] = None
