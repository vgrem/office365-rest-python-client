from office365.runtime.client_value import ClientValue


class RuleBasedSubjectSet(ClientValue):

    def __init__(self, rule: str = None):
        self.rule = rule
