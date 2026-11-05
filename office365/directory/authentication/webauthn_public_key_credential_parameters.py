from __future__ import annotations

from office365.runtime.client_value import ClientValue


class WebauthnPublicKeyCredentialParameters(ClientValue):
    alg: int | None = None
    type: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WebauthnPublicKeyCredentialParameters"
