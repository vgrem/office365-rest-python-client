from office365.runtime.client_value import ClientValue


class SPRuleUserInfo(ClientValue):
    def __init__(self, name: str = None, user_id: int = None):
        self.name = name
        self.user_id = user_id
