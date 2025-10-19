from office365.runtime.client_value import ClientValue


class TriggerAttribute(ClientValue):

    def __init__(self, name: str = None):
        self.name = name

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TriggerAttribute"
