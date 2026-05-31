from __future__ import annotations
from dataclasses import dataclass
from office365.runtime.client_value import ClientValue
from typing import Optional
from dataclasses import dataclass, field

@dataclass
class X509CertificateAuthorityScope(ClientValue):
    includeTargets: ClientValueCollection[IncludeTarget] = field(default_factory=lambda: ClientValueCollection(IncludeTarget))
    publicKeyInfrastructureIdentifier: str | None = None
    subjectKeyIdentifier: str | None = None

    @property
    def entity_type_name(self) -> str:
        return 'microsoft.graph.X509CertificateAuthorityScope'