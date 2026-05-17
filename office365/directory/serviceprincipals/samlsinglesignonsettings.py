from typing import Optional

from office365.runtime.client_value import ClientValue


class SamlSingleSignOnSettings(ClientValue):
    def __init__(self, relay_state: Optional[str] = None):
        self.relayState = relay_state

    @property
    def entity_type_name(self):
        return "microsoft.graph.SamlSingleSignOnSettings"
