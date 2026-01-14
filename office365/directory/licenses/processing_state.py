from office365.runtime.client_value import ClientValue


class LicenseProcessingState(ClientValue):
    def __init__(self, state: str = None):
        self.state = state

    ""

    @property
    def entity_type_name(self):
        return "microsoft.graph.LicenseProcessingState"
