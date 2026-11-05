from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.security.attacksimulations.oauthappscope import OAuthAppScope


class OAuthConsentAppDetail(ClientValue):
    appScope: OAuthAppScope = OAuthAppScope.unknown
    displayLogo: str | None = None
    displayName: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OAuthConsentAppDetail"
