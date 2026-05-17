from typing import Optional

from office365.runtime.client_value import ClientValue


class TriggerAttribute(ClientValue):
    def __init__(self, name: Optional[str] = None):
        self.name = name

    @property
    def entity_type_name(self):
        return "microsoft.graph.identityGovernance.TriggerAttribute"
