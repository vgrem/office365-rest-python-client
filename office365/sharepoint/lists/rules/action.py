from typing import Optional

from office365.runtime.client_value import ClientValue


class SPRuleAction(ClientValue):
    def __init__(self, action_params: Optional[dict] = None, action_type: Optional[int] = None):
        self.action_params = action_params
        self.action_type = action_type
