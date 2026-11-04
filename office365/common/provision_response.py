from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ProvisionResponse(ClientValue):
    challenge: str | None = None
    deviceId: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProvisionResponse"
