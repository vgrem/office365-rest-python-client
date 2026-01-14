from office365.runtime.client_value import ClientValue


class SPRuleAction(ClientValue):
    def __init__(self, action_params: dict = None, action_type: int = None):
        self.action_params = action_params
        self.action_type = action_type
