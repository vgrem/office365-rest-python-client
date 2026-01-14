from office365.runtime.client_value import ClientValue


class RulesProperties(ClientValue):
    def __init__(self, rules_key: str = None, rules_value: str = None):
        self.RulesKey = rules_key
        self.RulesValue = rules_value
