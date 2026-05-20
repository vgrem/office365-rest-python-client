from __future__ import annotations

from dataclasses import dataclass

from office365.directory.audit.initiatortype import InitiatorType
from office365.runtime.client_value import ClientValue


@dataclass
class Initiator(ClientValue):
    initiatorType: InitiatorType | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.Initiator"
