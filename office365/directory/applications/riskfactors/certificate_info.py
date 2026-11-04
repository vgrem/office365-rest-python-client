from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ApplicationRiskFactorCertificateInfo(ClientValue):
    hasBadCommonName: bool | None = None
    hasInsecureSignature: bool | None = None
    hasNoChainOfTrust: bool | None = None
    isDenylisted: bool | None = None
    isHostnameMismatch: bool | None = None
    isNotAfter: bool | None = None
    isNotBefore: bool | None = None
    isRevoked: bool | None = None
    isSelfSigned: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ApplicationRiskFactorCertificateInfo"
