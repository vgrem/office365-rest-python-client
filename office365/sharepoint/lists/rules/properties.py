from typing import Optional

from office365.runtime.client_value import ClientValue


class RulesProperties(ClientValue):
    def __init__(self, rules_key: Optional[str] = None, rules_value: Optional[str] = None):
        self.RulesKey = rules_key
        self.RulesValue = rules_value
