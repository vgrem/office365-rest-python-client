from __future__ import annotations

from enum import Enum


class AttestationEnforcement(Enum):
    disabled = "0"
    registrationOnly = "1"
    unknownFutureValue = "2"

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AttestationEnforcement"
