from office365.directory.audit.initiatortype import InitiatorType
from office365.runtime.client_value import ClientValue


class Initiator(ClientValue):

    def __init__(self, initiator_type: InitiatorType = None):
        self.initiatorType = initiator_type

    @property
    def entity_type_name(self):
        return "microsoft.graph.Initiator"
