from office365.runtime.client_value import ClientValue


class RestrictContentOrgWidePolicyUpdate(ClientValue):

    def __init__(self, is_policy_enabled: bool = None, justification: str = None):
        self.is_policy_enabled = is_policy_enabled
        self.justification = justification
