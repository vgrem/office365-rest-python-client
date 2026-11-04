from __future__ import annotations

from office365.directory.audit.initiatortype import InitiatorType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class Initiator(ClientValue):
    initiatorType: InitiatorType | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Initiator"
