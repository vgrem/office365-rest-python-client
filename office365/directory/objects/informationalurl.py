from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class InformationalUrl(ClientValue):
    logoUrl: str | None = None
    marketingUrl: str | None = None
    privacyStatementUrl: str | None = None
    supportUrl: str | None = None
    termsOfServiceUrl: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.InformationalUrl"
