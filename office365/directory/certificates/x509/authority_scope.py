from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.authentication.include_target import IncludeTarget
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class X509CertificateAuthorityScope(ClientValue):
    includeTargets: ClientValueCollection[IncludeTarget] = field(
        default_factory=lambda: ClientValueCollection(IncludeTarget)
    )
    publicKeyInfrastructureIdentifier: str | None = None
    subjectKeyIdentifier: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.X509CertificateAuthorityScope"
