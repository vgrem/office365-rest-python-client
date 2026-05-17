from office365.runtime.client_value import ClientValue
from typing import Optional


class RestrictContentOrgWidePolicyUpdate(ClientValue):
    def __init__(self, is_policy_enabled: Optional[bool] = None, justification: Optional[str] = None):
        self.is_policy_enabled = is_policy_enabled
        self.justification = justification
