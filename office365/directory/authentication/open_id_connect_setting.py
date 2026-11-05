from __future__ import annotations

from office365.runtime.client_value import ClientValue


class OpenIdConnectSetting(ClientValue):
    clientId: str | None = None
    discoveryUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OpenIdConnectSetting"
